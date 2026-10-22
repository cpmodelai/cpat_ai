Attribute VB_Name = "CPATScenarios"
Option Explicit
'==========================================================================
' CPAT-AI-Mitigation-Prototype v4.7 (module file CPATScenarios.bas): batch runs of scenario definitions into StoredResults (values).
'
' MTInputs holds one column per scenario: J = scenario 1 (baseline), K = scenario 2 (the live policy
' scenario that Mitigation group 2 calculates), L onwards = scenario definitions (row 4 "Run?" = Yes/No,
' row 5 number, row 6 name, rows 8-479 the inputs; v3.5: transport rows after 415).
'
' Public macros (Alt+F8):
'   RunAllScenarios       stores the baseline (only if not stored yet), then for every definition with
'                         Run? = Yes: copies it into the live column K, recalculates, runs the ETS goal seek
'                         when the definition applies a new ETS (and does not set "Override ETS price" =
'                         Yes), and stores the MTOutputs block of scenario 2 as values under the definition's
'                         number and name. Column K and the ETS override row are restored at the end.
'   StoreBaseline         (re)stores scenario 1 under ID 1 (replaces the stored baseline).
'   StoreLiveScenario     stores the live scenario 2 as it stands, under an ID you choose.
'   UpdateDataTables      v6.5: refreshes the linked data tabs (sheet DataLinks) for the country of Settings C4
'                         from the data source chosen on DataLinks (Power Query, one query per tab).
'   SolveETSLive          ETS goal seek for the live scenario only (fills its override row ets.ovr).
'   ClearStoredScenarios  deletes every stored scenario except the baseline.
'   CheckBatchRun         first-run test (run it once in Excel): checks that the macros find every sheet, row
'                         and column they use; compares this application's recalculation of the baseline with
'                         the stored baseline; reruns RunAll and compares every stored value with the values
'                         stored before the run (shipped: LibreOffice + Python). Report on sheet MacroCheck;
'                         Result = PASS when nothing differs by more than CHK_TOL (relative).
'
' ETS goal seek: legacy damped log-space iteration (OverrideETSFast / SolveFast) on the workbook's proposal
' row ets.next: p <- p x (proposal / p) ^ alpha, mixing 0.3 with the previous iterate, 5% centred 3-year
' smoothing, adaptive alpha; stops when the worst |covered / cap - 1| is below the tolerance. Same steps as
' ets_goalseek.py. v5.2: the settings are on sheet Manual inputs at the legacy addresses, read through the
' names ETSMaxIterations (E10), ETSStartFreshContinue (E11: StartFresh = start from the fast estimate ets.est;
' Continue = from the override row ets.ovr if it holds prices) and ETSErrorTolerance (E12); ETS_MAXITER and
' ETS_TOL apply only when a cell is not a positive number.
'==========================================================================

Private Const SH_MT As String = "ScenarioDefinition"
Private Const SH_MIT As String = "Mitigation"
Private Const SH_OUT As String = "LiveOutputs"
Private Const SH_SR As String = "StoredOutputs"
Private Const SH_CHECK As String = "Check, Variables, Lambdas"
Private Const CHK_FIRST As Long = 2268           ' MacroCheck: first report row (A = check, B = result)
Private Const CHK_TOL As Double = 0.000001
Private Const MT_ROW_RUN As Long = 4
Private Const MT_ROW_NUM As Long = 5
Private Const MT_ROW_NAME As Long = 6
Private Const MT_FIRST As Long = 8
Private Const MT_LAST As Long = 512
Private Const MT_ROW_ID As Long = 10          ' formula rows of every scenario column (kept in column K)
Private Const MT_ROW_IDNAME As Long = 12
Private Const MT_COL_PARAM As Long = 8        ' H: NameOfParameter
Private Const MT_COL_FIRST As Long = 10       ' J: scenario 1
Private Const MIT_ROW_SCEN As Long = 5
Private Const MIT_COL_FIRST As Long = 11      ' K: code column of scenario group 1
Private Const MIT_MAX_ROW As Long = 9000
Private Const OUT_COL_Y0 As Long = 6          ' MTOutputs: first year column (F)
Private Const SR_FIRST As Long = 6            ' StoredResults: first data row
Private Const SR_COL_Y0 As Long = 8           ' StoredResults: first year column (H)
Private Const NYEARS As Long = 20             ' 2022-2041 (the builder asserts NYEARS = years of the workbook)
Private Const LIVE_SCEN As Long = 2
Private Const BASE_SCEN As Long = 1
Private Const ETS_TOL As Double = 0.005
Private Const ETS_MAXITER As Long = 20
Private Const SH_DL As String = "ScenarioCompare"      ' v6.7: the data-source entries sit on the dashboard
Private Const SH_SC As String = "ScenarioCompare"      ' v6.7: the dashboard
Private Const MT_COL_CAP As Long = 52                   ' v6.7: last scenario column of ScenarioDefinition (AZ)
Private Const DL_MAXROWS As Long = 9000
' v7.1: Office-library constants by value (the embedded project references Excel and stdole only, so msoTrue,
' msoLineDash and msoLineSolid are undefined there: "Variable not defined" under Option Explicit)
Private Const MSO_TRUE As Long = -1
Private Const MSO_LINE_SOLID As Long = 1
Private Const MSO_LINE_DASH As Long = 4
Private Const DATA_FILE As String = "CPAT_Data_dummy_python.xlsx"
Private Const ALIAS_HEAD As String = "Code stem v7.1 (alias)"   ' v7.2: LiveOutputs alias column (codes R8)

'---------------------------------------------------------------- public macros
Public Sub RunAllScenarios()
    Dim n As Long
    n = RunAll()
    SortStoredOutputs                                     ' v6.7: like variables together, then the dashboard
    GroupBlankScenarios
    RefreshDashboard
    MsgBox n & " scenario definition(s) run and stored in " & SH_SR & ".", vbInformation, "CPAT scenarios"
End Sub

Public Sub StoreBaseline()
    If MsgBox("Replace the stored baseline (ID 1) by the current scenario 1 results?", vbYesNo + vbQuestion, _
              "CPAT scenarios") <> vbYes Then Exit Sub
    Recalc
    StoreScenario BASE_SCEN, BASE_SCEN, ""
    SortStoredOutputs
    RefreshDashboard
End Sub

Public Sub StoreLiveScenario()
    Dim v As Variant
    v = InputBox("Store the live scenario 2 under which ID? (an existing ID is replaced)", "CPAT scenarios", _
                 CStr(NextFreeId()))
    If Len(CStr(v)) = 0 Or Not IsNumeric(v) Then Exit Sub
    Recalc
    StoreScenario CLng(v), LIVE_SCEN, CStr(ThisWorkbook.Worksheets(SH_MT).Cells(MT_ROW_NAME, MTColumn(LIVE_SCEN)).Value)
    SortStoredOutputs
    RefreshDashboard
End Sub

Public Sub SolveETSLive()
    Dim w As Double
    w = SolveETS()
    MsgBox "ETS goal seek done: worst |covered / cap - 1| = " & Format(w, "0.0000"), vbInformation, "CPAT scenarios"
End Sub

Public Sub ClearStoredScenarios()
    If MsgBox("Delete every stored scenario except the baseline (ID 1)?", vbYesNo + vbQuestion, _
              "CPAT scenarios") <> vbYes Then Exit Sub
    KeepOnlyBaseline
End Sub

'---------------------------------------------------------------- v6.5: linked data tables (v6.7: entries on ScenarioCompare)
' ScenarioCompare holds the data-source dropdown (DataSource), the table of sources (DataSrcTable: name, kind, path or
' URL); Cover the table of linked tabs (DataLinkTable: prototype tab, data-workbook table, header cell, columns, rows
' (country / all), status). For every linked tab the macro writes the query text (path/URL and country as literals,
' so Power Query raises no privacy-firewall error), loads it in a staging sheet and copies it by column name
' (v7.1; before: a query table at the tab's header cell, columns in the data-workbook order).

Public Sub UpdateDataTables()
    Dim src As String, kind As String, loc As String, srcExpr As String, iso As String
    Dim lt As Range, r As Long, calc As Long, n As Long, msg As String, t0 As Double
    src = CStr(ThisWorkbook.Names("DataSource").RefersToRange.Value)
    If src Like "Embedded*" Then
        MsgBox "Data source is '" & src & "': the shipped data are used, nothing to update." & vbLf & _
               "Choose another source on " & SH_DL & " (Data source) first.", vbInformation, "CPAT data"
        Exit Sub
    End If
    If Not SourceOf(src, kind, loc) Then
        MsgBox "Data source '" & src & "' is not in the source table on " & SH_DL & ".", vbExclamation, "CPAT data"
        Exit Sub
    End If
    If kind = "file" Then
        If Len(loc) = 0 Then loc = FindLocalData()
        If Len(loc) = 0 Then Exit Sub
        srcExpr = "File.Contents(""" & loc & """)"
    Else
        If InStr(loc, "/:x:/") > 0 And InStr(loc, "download=1") = 0 Then   ' a Share link: ask for the file itself
            loc = loc & IIf(InStr(loc, "?") > 0, "&", "?") & "download=1"
        End If
        srcExpr = "Web.Contents(""" & loc & """)"
    End If
    ThisWorkbook.Names("DataUsed").RefersToRange.Value = loc
    ThisWorkbook.Names("DataSavedIn").RefersToRange.Value = ThisWorkbook.Path   ' v6.6: was CELL("filename")
    iso = UCase(CStr(ThisWorkbook.Names("CtryCode").RefersToRange.Value))
    calc = Application.Calculation
    Application.Calculation = xlCalculationManual
    Application.ScreenUpdating = False
    t0 = Timer
    On Error GoTo fail
    Set lt = ThisWorkbook.Names("DataLinkTable").RefersToRange
    For r = 1 To lt.Rows.Count
        If Len(CStr(lt.Cells(r, 1).Value)) > 0 Then
            n = RefreshLink(CStr(lt.Cells(r, 1).Value), CStr(lt.Cells(r, 2).Value), CStr(lt.Cells(r, 3).Value), _
                            CLng(lt.Cells(r, 4).Value), CStr(lt.Cells(r, 5).Value), srcExpr, iso, msg)
            lt.Cells(r, 6).Value = n & IIf(LCase(CStr(lt.Cells(r, 5).Value)) = "all", " rows (all), ", _
                                   " rows of " & iso & ", ") & src & ", " & Format(Now, "yyyy-mm-dd hh:nn")
            If n = 0 Then msg = msg & vbLf & "  " & lt.Cells(r, 1).Value & ": no rows for " & iso & _
                                " (shipped data kept)"
        End If
    Next r
    ThisWorkbook.Names("DataLastUpdate").RefersToRange.Value = src & " (" & iso & "), " & Format(Now, "yyyy-mm-dd hh:nn")
    Application.Calculation = calc
    Application.ScreenUpdating = True
    Application.CalculateFull
    MsgBox "Linked data tables updated from '" & src & "' for " & iso & " in " & Format(Timer - t0, "0.0") & " s." & _
           IIf(Len(msg) > 0, vbLf & "Warning:" & msg, ""), vbInformation, "CPAT data"
    Exit Sub
fail:
    Application.Calculation = calc
    Application.ScreenUpdating = True
    MsgBox "Update failed: " & Err.Description & vbLf & vbLf & _
           "SharePoint: sign in with 'Organizational account' when asked; if a Share link fails, open the data " & _
           "file in Excel desktop, File > Info > Copy path, and paste that path in the source table on " & SH_DL & _
           "." & vbLf & "Local file: check the path in the source table (blank = searched next to this workbook).", _
           vbExclamation, "CPAT data"
End Sub

Private Function SourceOf(ByVal src As String, ByRef kind As String, ByRef loc As String) As Boolean
    Dim st As Range, r As Long
    Set st = ThisWorkbook.Names("DataSrcTable").RefersToRange
    For r = 1 To st.Rows.Count
        If CStr(st.Cells(r, 1).Value) = src Then
            kind = LCase(CStr(st.Cells(r, 2).Value))
            loc = Trim(CStr(st.Cells(r, 3).Value))
            SourceOf = True
            Exit Function
        End If
    Next r
End Function

Private Function FindLocalData() As String
    ' the repository layout: <repo>\data\workbooks\CPAT_Data_dummy_python.xlsx; the workbook in excel_ai\ or
    ' excel_ai\mitigation\, or the data file next to the workbook
    Dim cands As Variant, c As Variant, p As String, f As Variant
    p = ThisWorkbook.Path
    If Left(p, 4) <> "http" Then
        cands = Array(p & "\" & DATA_FILE, p & "\data\workbooks\" & DATA_FILE, _
                      p & "\..\data\workbooks\" & DATA_FILE, p & "\..\..\data\workbooks\" & DATA_FILE, _
                      p & "\..\..\..\data\workbooks\" & DATA_FILE)
        For Each c In cands
            If Len(Dir(CStr(c))) > 0 Then
                FindLocalData = CreateObject("Scripting.FileSystemObject").GetAbsolutePathName(CStr(c))
                Exit Function
            End If
        Next c
    End If
    f = Application.GetOpenFilename("Excel files (*.xlsx),*.xlsx", , "Find the CPAT data workbook (" & DATA_FILE & ")")
    If VarType(f) = vbString Then FindLocalData = CStr(f)
End Function

Private Function RefreshLink(ByVal tabName As String, ByVal tbl As String, ByVal hdr As String, ByVal ncol As Long, _
                             ByVal rowsOf As String, ByVal srcExpr As String, ByVal iso As String, _
                             ByRef warn As String) As Long
    ' v7.1: the query loads into a staging sheet; its columns are copied to the tab by the names in the tab's own
    ' header row (any column order in the data workbook; the header row and the formula columns of the tab stay),
    ' rows of the country only ("country") or every row ("all"); with no rows the shipped data stay
    Dim m As String, qn As String, q As Object, ws As Worksheet, st As Worksheet, lo As ListObject
    Dim hd As Variant, sh As Variant, dat As Variant, outv() As Variant, n As Long, i As Long, j As Long, k As Long
    Dim miss As String, cn As Object, hadAlerts As Boolean
    qn = "q_" & tabName
    m = "let" & vbLf & _
        "    Book = Excel.Workbook(" & srcExpr & ", true, true)," & vbLf & _
        "    T = Book{[Item=""" & tbl & """, Kind=""Table""]}[Data]," & vbLf
    If LCase(rowsOf) = "all" Then
        m = m & "    Rows = T," & vbLf
    Else
        m = m & "    Rows = Table.SelectRows(T, each [FilterISO3] = """ & iso & """)," & vbLf
    End If
    m = m & "    Out = Table.RemoveColumns(Rows, {""FilterISO3""}, MissingField.Ignore)" & vbLf & "in" & vbLf & "    Out"
    On Error Resume Next
    Set q = ThisWorkbook.Queries(qn)
    On Error GoTo 0
    If q Is Nothing Then
        ThisWorkbook.Queries.Add qn, m
    Else
        q.Formula = m
    End If
    Set ws = ThisWorkbook.Worksheets(tabName)
    hadAlerts = Application.DisplayAlerts
    Application.DisplayAlerts = False
    On Error Resume Next                        ' a staging sheet left by an interrupted update
    ThisWorkbook.Worksheets("zStage").Delete
    On Error GoTo 0
    Application.DisplayAlerts = hadAlerts
    Set st =ThisWorkbook.Worksheets.Add(After:=ThisWorkbook.Worksheets(ThisWorkbook.Worksheets.Count))
    st.Name = "zStage"
    On Error GoTo cleanup
    Set lo = st.ListObjects.Add(SourceType:=0, Source:="OLEDB;Provider=Microsoft.Mashup.OleDb.1;" & _
             "Data Source=$Workbook$;Location=" & qn & ";Extended Properties=""""", Destination:=st.Range("A1"))
    With lo.QueryTable
        .CommandType = xlCmdSql
        .CommandText = Array("SELECT * FROM [" & qn & "]")
        .BackgroundQuery = False
        .Refresh BackgroundQuery:=False
    End With
    n = lo.ListRows.Count
    If n > DL_MAXROWS Then Err.Raise 1004, , tabName & ": more than " & DL_MAXROWS & " rows"
    If n > 0 Then
        sh = lo.HeaderRowRange.Value
        dat = lo.DataBodyRange.Value
        hd = ws.Range(hdr).Resize(1, ncol).Value
        ReDim outv(1 To n, 1 To ncol)
        For j = 1 To ncol
            k = 0
            For i = 1 To UBound(sh, 2)
                If HeaderKey(sh(1, i)) = HeaderKey(hd(1, j)) Then k = i: Exit For
            Next i
            If k > 0 Then
                For i = 1 To n
                    outv(i, j) = dat(i, k)
                Next i
            ElseIf Len(HeaderKey(hd(1, j))) > 0 Then
                miss = miss & IIf(Len(miss) > 0, ", ", "") & HeaderKey(hd(1, j))
            End If
        Next j
        ws.Range(hdr).Offset(1, 0).Resize(DL_MAXROWS, ncol).ClearContents
        ws.Range(hdr).Offset(1, 0).Resize(n, ncol).Value = outv
        If Len(miss) > 0 Then warn = warn & vbLf & "  " & tabName & ": columns not in " & tbl & " (left blank): " & miss
    End If
    RefreshLink = n
cleanup:
    hadAlerts = Application.DisplayAlerts
    Application.DisplayAlerts = False
    For Each cn In ThisWorkbook.Connections
        If InStr(cn.Name, qn) > 0 Then cn.Delete
    Next cn
    st.Delete
    Application.DisplayAlerts = hadAlerts
    If Err.Number <> 0 Then Err.Raise Err.Number, , Err.Description
End Function

Private Function HeaderKey(ByVal v As Variant) As String
    ' a header cell as text: numbers without decimals (year columns), trimmed
    If IsNumeric(v) And Not IsEmpty(v) And VarType(v) <> vbString Then
        HeaderKey = CStr(CDbl(v))
    Else
        HeaderKey = Trim(CStr(v))
    End If
End Function

Private Sub Recalc()
    ' v7.1: recalculate twice. In Excel the second pass finds nothing left to calculate (no cost); LibreOffice, where
    ' the macros are tested, leaves differences of up to 2e-3 after one pass (excel_ai/NORMS.md 3i.2)
    Application.Calculate
    Application.Calculate
End Sub

Public Sub CalculationOn()
    Application.Calculation = xlCalculationAutomatic
    Application.CalculateFull
End Sub

Public Sub CalculationOff()
    Application.Calculation = xlCalculationManual
End Sub

' v6.6: the workbook ships with its values and opens in manual calculation (no recalculation on open)
Public Sub RecalculateNow()
    Dim t As Double
    t = Timer
    Application.StatusBar = "Recalculating CPAT..."
    Application.CalculateFull
    Application.StatusBar = False
    RefreshDashboard                                      ' v6.7: charts follow the scenarios with results
    MsgBox "Recalculated in " & Format(Timer - t, "0.0") & " seconds.", vbInformation, "CPAT"
End Sub

Public Sub ToggleRecalculation()
    If Application.Calculation = xlCalculationManual Then
        Application.Calculation = xlCalculationAutomatic
        MsgBox "Recalculation is ON (automatic). Every change recalculates the workbook." & vbCrLf & _
               "Note: Excel applies this to every open workbook.", vbInformation, "CPAT"
    Else
        Application.Calculation = xlCalculationManual
        MsgBox "Recalculation is OFF (manual). Use 'Recalculate now' to update the results.", vbInformation, "CPAT"
    End If
End Sub

'---------------------------------------------------------------- batch run (no dialogs: also used by tests)
Public Function RunAll() As Long
    Dim mt As Worksheet, liveCol As Long, c As Long, r As Long, n As Long
    Dim savedVal(1 To MT_LAST) As Variant, savedIsF(1 To MT_LAST) As Boolean
    Dim ovr As Long, ovrBase As Long, savedOvr(1 To NYEARS) As Variant, j As Long
    Set mt = ThisWorkbook.Worksheets(SH_MT)
    liveCol = MTColumn(LIVE_SCEN)
    For r = 1 To MT_LAST                                  ' save the live column (formulas and values)
        savedIsF(r) = mt.Cells(r, liveCol).HasFormula
        If savedIsF(r) Then savedVal(r) = mt.Cells(r, liveCol).Formula Else savedVal(r) = mt.Cells(r, liveCol).Value
    Next r
    ovr = MitRow("ets.ovr")
    ovrBase = MitBaseCol(LIVE_SCEN)
    For j = 1 To NYEARS
        savedOvr(j) = ThisWorkbook.Worksheets(SH_MIT).Cells(ovr, ovrBase + j - 1).Value
    Next j
    Dim calcWas As Long
    calcWas = Application.Calculation                     ' v6.6: restored at the end (the workbook ships manual)
    On Error Resume Next
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    On Error GoTo 0
    Recalc
    If FindStored(BASE_SCEN) = 0 Then StoreScenario BASE_SCEN, BASE_SCEN, ""
    c = liveCol + 1
    Do While Not IsEmpty(mt.Cells(MT_ROW_NUM, c).Value)
        If UCase(Left(Trim(CStr(mt.Cells(MT_ROW_RUN, c).Value)), 1)) = "Y" Then
            For r = MT_FIRST To MT_LAST
                If r <> MT_ROW_ID And r <> MT_ROW_IDNAME Then mt.Cells(r, liveCol).Value = mt.Cells(r, c).Value
            Next r
            mt.Cells(MT_ROW_NAME, liveCol).Value = mt.Cells(MT_ROW_NAME, c).Value
            For j = 1 To NYEARS
                ThisWorkbook.Worksheets(SH_MIT).Cells(ovr, ovrBase + j - 1).ClearContents
            Next j
            Recalc
            If NeedsETS(liveCol) Then SolveETS
            StoreScenario CLng(mt.Cells(MT_ROW_NUM, c).Value), LIVE_SCEN, CStr(mt.Cells(MT_ROW_NAME, c).Value)
            n = n + 1
        End If
        c = c + 1
    Loop
    For r = 1 To MT_LAST                                  ' restore the live column and the override row
        If savedIsF(r) Then
            mt.Cells(r, liveCol).Formula = savedVal(r)
        ElseIf IsEmpty(savedVal(r)) Then
            mt.Cells(r, liveCol).ClearContents
        Else
            mt.Cells(r, liveCol).Value = savedVal(r)
        End If
    Next r
    For j = 1 To NYEARS
        If IsEmpty(savedOvr(j)) Then
            ThisWorkbook.Worksheets(SH_MIT).Cells(ovr, ovrBase + j - 1).ClearContents
        Else
            ThisWorkbook.Worksheets(SH_MIT).Cells(ovr, ovrBase + j - 1).Value = savedOvr(j)
        End If
    Next j
    On Error Resume Next
    Application.Calculation = calcWas
    Application.ScreenUpdating = True
    On Error GoTo 0
    Recalc
    RunAll = n
End Function

'---------------------------------------------------------------- ETS goal seek on the live scenario
Public Function SolveETS() As Double
    Dim mit As Worksheet, mt As Worksheet, liveCol As Long, rO As Long, rE As Long, rN As Long, rG As Long, rC As Long
    Dim b As Long, j As Long, it As Long, hasOvr As Boolean, hasPrev As Boolean
    Dim p(1 To NYEARS) As Double, pPrev(1 To NYEARS) As Double, pNew(1 To NYEARS) As Double
    Dim resp(1 To NYEARS) As Double, gap As Double, cap As Double, sm As Double
    Dim alpha As Double, worst As Double, prevWorst As Double, converged As Boolean
    Dim maxIt As Long, tol As Double, fresh As Boolean
    maxIt = CLng(Num(NamedValue("ETSMaxIterations")))     ' v5.2: Manual inputs E10:E12 (legacy addresses)
    If maxIt < 1 Then maxIt = ETS_MAXITER
    tol = Num(NamedValue("ETSErrorTolerance"))
    If tol <= 0 Then tol = ETS_TOL
    fresh = LCase(Left(CStr(NamedValue("ETSStartFreshContinue")), 5)) = "start"
    Set mit = ThisWorkbook.Worksheets(SH_MIT)
    Set mt = ThisWorkbook.Worksheets(SH_MT)
    liveCol = MTColumn(LIVE_SCEN)
    mt.Cells(MTParamRow("D_ETSPriceOverride"), liveCol).Value = "Yes"
    rO = MitRow("ets.ovr"): rE = MitRow("ets.est"): rN = MitRow("ets.next")
    rG = MitRow("co2.gap"): rC = MitRow("co2.cap")
    b = MitBaseCol(LIVE_SCEN)
    Recalc
    For j = 1 To NYEARS
        p(j) = Num(mit.Cells(rO, b + j - 1).Value)
        If p(j) <> 0 Then hasOvr = True
    Next j
    If fresh Then hasOvr = False
    If Not hasOvr Then
        For j = 1 To NYEARS
            p(j) = Num(mit.Cells(rE, b + j - 1).Value)
        Next j
    End If
    alpha = 1#
    prevWorst = 1E+300
    For it = 1 To maxIt
        For j = 1 To NYEARS
            mit.Cells(rO, b + j - 1).Value = p(j)
        Next j
        Recalc
        worst = 0#
        For j = 1 To NYEARS
            resp(j) = Num(mit.Cells(rN, b + j - 1).Value)
            gap = Num(mit.Cells(rG, b + j - 1).Value)
            cap = Num(mit.Cells(rC, b + j - 1).Value)
            If cap > 0 And Abs(gap) > worst Then worst = Abs(gap)
        Next j
        If worst < tol Then
            converged = True
            Exit For
        End If
        For j = 1 To NYEARS
            pNew(j) = LogStep(p(j), resp(j), alpha)
            If hasPrev Then pNew(j) = 0.7 * pNew(j) + 0.3 * pPrev(j)
        Next j
        For j = 1 To NYEARS                               ' 5% weight on a centred 3-year moving average
            If j = 1 Then
                sm = (pNew(1) + pNew(2)) / 2
            ElseIf j = NYEARS Then
                sm = (pNew(NYEARS - 1) + pNew(NYEARS)) / 2
            Else
                sm = (pNew(j - 1) + pNew(j) + pNew(j + 1)) / 3
            End If
            resp(j) = 0.95 * pNew(j) + 0.05 * sm          ' resp reused as the smoothed vector
        Next j
        For j = 1 To NYEARS
            If resp(j) < 0 Then resp(j) = p(j)
        Next j
        If worst > prevWorst Then
            alpha = alpha * 0.5
            If alpha < 0.0625 Then alpha = 0.0625
        ElseIf worst < 0.5 * prevWorst Then
            alpha = alpha * 1.2
            If alpha > 1# Then alpha = 1#
        End If
        prevWorst = worst
        For j = 1 To NYEARS
            pPrev(j) = p(j)
            p(j) = resp(j)
        Next j
        hasPrev = True
    Next it
    If Not converged Then                                 ' leave the last step's prices in place
        For j = 1 To NYEARS
            mit.Cells(rO, b + j - 1).Value = p(j)
        Next j
        Recalc
    End If
    SolveETS = worst
End Function

Private Function NamedValue(ByVal nm As String) As Variant
    NamedValue = ThisWorkbook.Names(nm).RefersToRange.Value  ' v5.2: a single-cell workbook name
End Function

Private Function LogStep(ByVal pc As Double, ByVal pr As Double, ByVal alpha As Double) As Double
    If pc <= 0 Or pr <= 0 Then
        LogStep = pc + alpha * (pr - pc)
        If LogStep < 0 Then LogStep = 0
    Else
        LogStep = pc * (pr / pc) ^ alpha
    End If
End Function

'---------------------------------------------------------------- storing results as values
Private Sub StoreScenario(ByVal id As Long, ByVal srcScen As Long, ByVal nm As String)
    Dim mo As Worksheet, sr As Worksheet, h As Long, r As Long, n As Long, d As Long, k As Long, j As Long
    Dim code As String, country As String, stamp As Date
    UpgradeStoredCodes                                    ' v7.2: v7.1 stems renamed first
    Set mo = ThisWorkbook.Worksheets(SH_OUT)
    Set sr = ThisWorkbook.Worksheets(SH_SR)
    For r = 5 To 2000                                     ' header row of the MTOutputs block
        If CStr(mo.Cells(r, 1).Value) = "Scenario block" Then
            If Num(mo.Cells(r, 5).Value) = srcScen Then
                h = r
                Exit For
            End If
        End If
    Next r
    If h = 0 Then Err.Raise vbObjectError + 1, , "No MTOutputs block for scenario " & srcScen
    If Len(nm) = 0 Then nm = CStr(mo.Cells(h, 3).Value)
    Do While Len(CStr(mo.Cells(h + 1 + n, 2).Value)) > 0
        n = n + 1
    Loop
    DeleteStored id                                       ' v6.7: the ID's rows wherever they are (sorted sheet)
    d = FirstFreeRow()
    code = CStr(mo.Cells(h + 1, 1).Value)
    country = Left(code, InStr(code, ".") - 1)
    stamp = Now
    For k = 0 To n - 1
        sr.Cells(d + k, 1).Value = id
        sr.Cells(d + k, 2).Value = nm
        sr.Cells(d + k, 3).Value = mo.Cells(h + 1 + k, 2).Value
        sr.Cells(d + k, 4).Value = country & "." & CStr(mo.Cells(h + 1 + k, 2).Value) & "." & id
        sr.Cells(d + k, 5).Value = mo.Cells(h + 1 + k, 3).Value
        sr.Cells(d + k, 6).Value = mo.Cells(h + 1 + k, 4).Value
        sr.Cells(d + k, 7).Value = stamp
        For j = 1 To NYEARS
            sr.Cells(d + k, SR_COL_Y0 + j - 1).Value = mo.Cells(h + 1 + k, OUT_COL_Y0 + j - 1).Value
        Next j
    Next k
End Sub

Private Sub DeleteStored(ByVal id As Long)
    ' v6.7: delete every stored row of the ID and close the gaps (the rows may be anywhere after a sort)
    Dim sr As Worksheet, r As Long, last As Long
    Set sr = ThisWorkbook.Worksheets(SH_SR)
    last = FirstFreeRow() - 1
    For r = last To SR_FIRST Step -1
        If Num(sr.Cells(r, 1).Value) = id And Len(CStr(sr.Cells(r, 3).Value)) > 0 Then
            sr.Range(sr.Cells(r, 1), sr.Cells(r, SR_COL_Y0 + NYEARS - 1)).Delete Shift:=xlUp
        End If
    Next r
End Sub

'---------------------------------------------------------------- v7.2 (codes R8): v7.1 code stems accepted
Public Sub UpgradeStoredCodes()
    ' stored rows of v7.1 carry the old prototype code stems: each is renamed to its protocol stem through the alias column
    ' of LiveOutputs ("Code stem v7.1 (alias)"), and its output code with it; kept for one release
    Dim mo As Worksheet, sr As Worksheet, ac As Long, c As Long, r As Long, q As Long, last As Long, n As Long
    Dim olds() As String, news() As String, s As String, cd As String
    Set mo = ThisWorkbook.Worksheets(SH_OUT)
    Set sr = ThisWorkbook.Worksheets(SH_SR)
    For c = 1 To 200
        If CStr(mo.Cells(4, c).Value) = ALIAS_HEAD Then
            ac = c
            Exit For
        End If
    Next c
    If ac = 0 Then Exit Sub
    ReDim olds(1 To 1)
    ReDim news(1 To 1)
    For r = 5 To 2000                                     ' the aliases of the first block (every block is the same)
        If CStr(mo.Cells(r, 1).Value) = "Scenario block" And n > 0 Then Exit For
        If Len(CStr(mo.Cells(r, ac).Value)) > 0 Then
            n = n + 1
            ReDim Preserve olds(1 To n)
            ReDim Preserve news(1 To n)
            olds(n) = CStr(mo.Cells(r, ac).Value)
            news(n) = CStr(mo.Cells(r, 2).Value)
        End If
    Next r
    If n = 0 Then Exit Sub
    last = FirstFreeRow() - 1
    For r = SR_FIRST To last
        s = CStr(sr.Cells(r, 3).Value)
        For q = 1 To n
            If s = olds(q) Then
                cd = CStr(sr.Cells(r, 4).Value)
                sr.Cells(r, 3).Value = news(q)
                If InStr(cd, ".") > 0 Then sr.Cells(r, 4).Value = Left(cd, InStr(cd, ".") - 1) & "." & news(q) & "." & sr.Cells(r, 1).Value
                Exit For
            End If
        Next q
    Next r
End Sub

'---------------------------------------------------------------- v6.7: dashboard helpers
Public Sub SortStoredOutputs()
    ' like variables together: by code stem, then scenario ID (every lookup matches the output code, so any order works)
    Dim sr As Worksheet, last As Long
    Set sr = ThisWorkbook.Worksheets(SH_SR)
    last = FirstFreeRow() - 1
    If last <= SR_FIRST Then Exit Sub
    With sr.Sort
        .SortFields.Clear
        .SortFields.Add Key:=sr.Range(sr.Cells(SR_FIRST, 3), sr.Cells(last, 3)), Order:=xlAscending
        .SortFields.Add Key:=sr.Range(sr.Cells(SR_FIRST, 1), sr.Cells(last, 1)), Order:=xlAscending
        .SetRange sr.Range(sr.Cells(SR_FIRST, 1), sr.Cells(last, SR_COL_Y0 + NYEARS - 1))
        .Header = xlNo
        .Apply
    End With
End Sub

Public Sub GroupBlankScenarios()
    ' scenario columns of ScenarioDefinition with no name: grouped and collapsed (unhide with the outline + button)
    Dim mt As Worksheet, c As Long, blank As Boolean
    Set mt = ThisWorkbook.Worksheets(SH_MT)
    For c = MT_COL_FIRST To MT_COL_CAP
        blank = Len(Trim(CStr(mt.Cells(MT_ROW_NAME, c).Value))) = 0
        mt.Columns(c).OutlineLevel = IIf(blank, 2, 1)
        mt.Columns(c).Hidden = blank
    Next c
End Sub

Public Sub RefreshDashboard()
    ' the charts of ScenarioCompare show only the scenarios with results in the chosen source (Live / Stored); the
    ' table rows of the others are hidden. Chart i follows row i of SCChartCfg: kind, first row, last row, year row,
    ' first column, last column, title row.
    Dim ws As Worksheet, cfg As Range, i As Long, ch As Chart, r As Long, s As Series, has As Boolean
    Dim r0 As Long, r1 As Long, hr As Long, c0 As Long, c1 As Long, tr As Long
    Set ws = ThisWorkbook.Worksheets(SH_SC)
    Set cfg = ThisWorkbook.Names("SCChartCfg").RefersToRange
    Application.ScreenUpdating = False
    On Error GoTo done
    For i = 1 To cfg.Rows.Count
        If i > ws.ChartObjects.Count Then Exit For
        Set ch = ws.ChartObjects(i).Chart
        r0 = cfg.Cells(i, 2).Value: r1 = cfg.Cells(i, 3).Value: hr = cfg.Cells(i, 4).Value
        c0 = cfg.Cells(i, 5).Value: c1 = cfg.Cells(i, 6).Value: tr = cfg.Cells(i, 7).Value
        If CStr(cfg.Cells(i, 1).Value) = "line" Then
            Do While ch.SeriesCollection.Count > 0
                ch.SeriesCollection(1).Delete
            Loop
            For r = r0 To r1
                has = Application.WorksheetFunction.Count(ws.Range(ws.Cells(r, c0), ws.Cells(r, c1))) > 0
                ws.Rows(r).Hidden = Not has
                If has Then
                    Set s = ch.SeriesCollection.NewSeries
                    s.Name = "='" & SH_SC & "'!" & ws.Cells(r, 3).Address
                    s.Values = ws.Range(ws.Cells(r, c0), ws.Cells(r, c1))
                    s.XValues = ws.Range(ws.Cells(hr, c0), ws.Cells(hr, c1))
                    StyleSeries s, r - r0 + 1
                End If
            Next r
            ch.HasTitle = True
            ch.ChartTitle.Text = CStr(ws.Cells(tr, 2).Value) & " (" & CStr(ws.Cells(tr, 3).Value) & ")"
        End If
    Next i
done:
    Application.ScreenUpdating = True
End Sub

Private Sub StyleSeries(s As Series, ByVal slot As Long)
    Dim pal As Variant
    pal = Array(RGB(64, 64, 64), RGB(31, 119, 180), RGB(255, 127, 14), RGB(44, 160, 44), RGB(214, 39, 40), _
                RGB(148, 103, 189), RGB(140, 86, 75), RGB(227, 119, 194), RGB(23, 190, 207), RGB(188, 189, 34))
    s.MarkerStyle = xlMarkerStyleNone
    s.Format.Line.Visible = MSO_TRUE
    s.Format.Line.ForeColor.RGB = pal((slot - 1) Mod 10)
    s.Format.Line.Weight = IIf(slot = 1, 2.25, 1.75)
    s.Format.Line.DashStyle = IIf(slot = 1, MSO_LINE_DASH, MSO_LINE_SOLID)
End Sub

Private Sub KeepOnlyBaseline()
    Dim sr As Worksheet, r As Long, w As Long, c As Long, last As Long
    Set sr = ThisWorkbook.Worksheets(SH_SR)
    last = FirstFreeRow() - 1
    w = SR_FIRST
    For r = SR_FIRST To last
        If Num(sr.Cells(r, 1).Value) = BASE_SCEN Then
            If w <> r Then
                For c = 1 To SR_COL_Y0 + NYEARS - 1
                    sr.Cells(w, c).Value = sr.Cells(r, c).Value
                Next c
            End If
            w = w + 1
        End If
    Next r
    If w <= last Then sr.Range(sr.Cells(w, 1), sr.Cells(last, SR_COL_Y0 + NYEARS - 1)).ClearContents
End Sub

'---------------------------------------------------------------- lookups
Private Function MTColumn(ByVal scen As Long) As Long
    Dim c As Long
    For c = MT_COL_FIRST To MT_COL_FIRST + 200
        If Num(ThisWorkbook.Worksheets(SH_MT).Cells(MT_ROW_NUM, c).Value) = scen Then
            MTColumn = c
            Exit Function
        End If
    Next c
    Err.Raise vbObjectError + 2, , "Scenario " & scen & " not found in MTInputs row 5"
End Function

Private Function MTParamRow(ByVal nm As String) As Long
    Dim r As Long
    For r = MT_FIRST To MT_LAST
        If CStr(ThisWorkbook.Worksheets(SH_MT).Cells(r, MT_COL_PARAM).Value) = nm Then
            MTParamRow = r
            Exit Function
        End If
    Next r
    Err.Raise vbObjectError + 3, , "Parameter " & nm & " not found in MTInputs column H"
End Function

Private Function NeedsETS(ByVal liveCol As Long) As Boolean
    Dim mt As Worksheet
    Set mt = ThisWorkbook.Worksheets(SH_MT)
    NeedsETS = UCase(Left(CStr(mt.Cells(MTParamRow("D_NewETS"), liveCol).Value), 3)) = "YES" And _
               UCase(Left(CStr(mt.Cells(MTParamRow("D_ETSPriceOverride"), liveCol).Value), 3)) <> "YES"
End Function

Private Function MitRow(ByVal code As String) As Long
    Dim r As Long
    For r = 1 To MIT_MAX_ROW
        If CStr(ThisWorkbook.Worksheets(SH_MIT).Cells(r, 1).Value) = code Then
            MitRow = r
            Exit Function
        End If
    Next r
    Err.Raise vbObjectError + 4, , "Row " & code & " not found in Mitigation column A"
End Function

Private Function MitBaseCol(ByVal scen As Long) As Long
    Dim c As Long
    For c = MIT_COL_FIRST To MIT_COL_FIRST + 2000
        If Num(ThisWorkbook.Worksheets(SH_MIT).Cells(MIT_ROW_SCEN, c).Value) = scen Then
            MitBaseCol = c + 1                            ' code column + 1 = base year
            Exit Function
        End If
    Next c
    Err.Raise vbObjectError + 5, , "Scenario group " & scen & " not found in Mitigation row 5"
End Function

Private Function FindStored(ByVal id As Long) As Long
    Dim sr As Worksheet, r As Long
    Set sr = ThisWorkbook.Worksheets(SH_SR)
    r = SR_FIRST
    Do While Len(CStr(sr.Cells(r, 3).Value)) > 0
        If Num(sr.Cells(r, 1).Value) = id Then
            FindStored = r
            Exit Function
        End If
        r = r + 1
    Loop
End Function

Private Function FirstFreeRow() As Long
    Dim sr As Worksheet, r As Long
    Set sr = ThisWorkbook.Worksheets(SH_SR)
    r = SR_FIRST
    Do While Len(CStr(sr.Cells(r, 3).Value)) > 0
        r = r + 1
    Loop
    FirstFreeRow = r
End Function

Private Function NextFreeId() As Long
    Dim sr As Worksheet, r As Long, m As Long
    Set sr = ThisWorkbook.Worksheets(SH_SR)
    m = 99
    r = SR_FIRST
    Do While Len(CStr(sr.Cells(r, 3).Value)) > 0
        If Num(sr.Cells(r, 1).Value) > m Then m = Num(sr.Cells(r, 1).Value)
        r = r + 1
    Loop
    NextFreeId = m + 1
End Function

Private Function Num(ByVal v As Variant) As Double
    If IsError(v) Then
        Num = 0
    ElseIf IsNumeric(v) And Not IsEmpty(v) Then
        Num = CDbl(v)
    Else
        Num = 0
    End If
End Function

'---------------------------------------------------------------- first-run test
Public Sub CheckBatchRun()
    Dim w As Double
    w = CheckBatch()
    If w < 0 Then
        MsgBox "Batch check FAILED: the macros cannot find what they need. See sheet " & SH_CHECK & ".", _
               vbExclamation, "CPAT scenarios"
    Else
        MsgBox "Batch check done. Result: " & CStr(ThisWorkbook.Worksheets(SH_CHECK).Cells(CHK_FIRST, 2).Value) & _
               ". Largest relative difference vs the stored values: " & Format(w, "0.0E+00") & _
               ". Details on sheet " & SH_CHECK & ".", vbInformation, "CPAT scenarios"
    End If
End Sub

Public Function CheckBatch() As Double
    Dim mc As Worksheet, sr As Worksheet, mo As Worksheet, wr As Long, nFail As Long, msg As String, v As Long
    Dim items As Variant, i As Long, n As Long, m As Long, j As Long, r As Long, q As Long, h As Long, k As Long
    Dim oldId() As Double, oldStem() As String, oldVal() As Double, newId() As Double, newStem() As String
    Dim newVal() As Double, d As Double, worst As Double, worstB As Double, nBad As Long, nCells As Long
    Dim nMissing As Long, hit As Long, stem As String, nEts As Long, worstEts As Double   ' v5.2: new-ETS definitions
    Set mc = ThisWorkbook.Worksheets(SH_CHECK)
    Set sr = ThisWorkbook.Worksheets(SH_SR)
    Set mo = ThisWorkbook.Worksheets(SH_OUT)
    mc.Range(mc.Cells(CHK_FIRST, 1), mc.Cells(CHK_FIRST + 300, 2)).ClearContents
    wr = CHK_FIRST + 1                                    ' row CHK_FIRST: overall result, written last
    Note mc, wr, "Started", Format(Now, "yyyy-mm-dd hh:mm:ss") & " in " & HostName()
    ' 1. everything the macros look up
    items = Array("mtcol", "1", "MTInputs: column of scenario 1 (baseline)", _
                  "mtcol", "2", "MTInputs: column of scenario 2 (live)", _
                  "mtparam", "D_NewETS", "MTInputs: row of D_NewETS", _
                  "mtparam", "D_ETSPriceOverride", "MTInputs: row of D_ETSPriceOverride", _
                  "mitbase", "2", "Mitigation: base-year column of scenario group 2", _
                  "mitrow", "ets.ovr", "Mitigation: row ets.ovr (ETS override prices)", _
                  "mitrow", "ets.est", "Mitigation: row ets.est (fast estimate)", _
                  "mitrow", "ets.next", "Mitigation: row ets.next (next price proposal)", _
                  "mitrow", "co2.gap", "Mitigation: row co2.gap (covered / cap - 1)", _
                  "mitrow", "co2.cap", "Mitigation: row co2.cap (ETS cap)", _
                  "outblock", "1", "MTOutputs: block of scenario 1", _
                  "outblock", "2", "MTOutputs: block of scenario 2", _
                  "name", "ETSMaxIterations", "Manual inputs: ETS goal seek, maximum iterations (E10)", _
                  "name", "ETSStartFreshContinue", "Manual inputs: ETS goal seek, start fresh or continue (E11)", _
                  "name", "ETSErrorTolerance", "Manual inputs: ETS goal seek, maximum error (E12)")
    For i = 0 To UBound(items) Step 3
        msg = ""
        v = Probe(CStr(items(i)), CStr(items(i + 1)), msg)
        If v > 0 Then
            Note mc, wr, CStr(items(i + 2)), "OK (" & v & ")"
        Else
            Note mc, wr, CStr(items(i + 2)), "FAIL: " & msg
            nFail = nFail + 1
        End If
    Next i
    If nFail > 0 Then
        mc.Cells(CHK_FIRST, 1).Value = "Result"
        mc.Cells(CHK_FIRST, 2).Value = "FAIL: " & nFail & " lookup(s) not found (see below)"
        CheckBatch = -1
        Exit Function
    End If
    ' 2. snapshot of the stored values
    n = ReadStored(oldId, oldStem, oldVal)
    Note mc, wr, "Stored rows before the run", CStr(n)
    ' 3. the baseline as this application calculates it vs the stored baseline (ID 1)
    Recalc
    h = OutBlockRow(BASE_SCEN)
    k = 0
    Do While Len(CStr(mo.Cells(h + 1 + k, 2).Value)) > 0
        stem = CStr(mo.Cells(h + 1 + k, 2).Value)
        hit = 0
        For r = 1 To n
            If oldId(r) = BASE_SCEN And oldStem(r) = stem Then hit = r
        Next r
        If hit = 0 Then
            nMissing = nMissing + 1
        Else
            For j = 1 To NYEARS
                d = RelDiff(Num(mo.Cells(h + 1 + k, OUT_COL_Y0 + j - 1).Value), oldVal(hit, j))
                If d > worstB Then worstB = d
            Next j
        End If
        k = k + 1
    Loop
    Note mc, wr, "Baseline recalculated here vs stored ID 1: rows compared", CStr(k - nMissing)
    Note mc, wr, "Baseline: largest relative difference", Format(worstB, "0.0E+00")
    ' 4. batch run and comparison of every stored value
    Note mc, wr, "RunAll: definitions run and stored", CStr(RunAll())
    m = ReadStored(newId, newStem, newVal)
    For r = 1 To n
        hit = 0
        For q = 1 To m
            If newId(q) = oldId(r) And newStem(q) = oldStem(r) Then hit = q
        Next q
        If hit = 0 Then
            nMissing = nMissing + 1
            Note mc, wr, "Missing after the run", "ID " & oldId(r) & ", " & oldStem(r)
        ElseIf NeedsETS(MTColumn(CLng(oldId(r)))) Then
            ' v5.2: a new-ETS definition is stored by the build at the fast price estimate (no goal seek, user rule
            ' 2026-10-17); the run goal-seeks it, so it is reported, not compared
            For j = 1 To NYEARS
                d = RelDiff(newVal(hit, j), oldVal(r, j))
                nEts = nEts + 1
                If d > worstEts Then worstEts = d
            Next j
        Else
            For j = 1 To NYEARS
                d = RelDiff(newVal(hit, j), oldVal(r, j))
                nCells = nCells + 1
                If d > worst Then worst = d
                If d > CHK_TOL Then nBad = nBad + 1
            Next j
        End If
    Next r
    If nEts > 0 Then Note mc, wr, "New-ETS definitions (stored without goal seek, re-solved by the run; not compared): " & _
                          "cells, largest relative difference", CStr(nEts) & ", " & Format(worstEts, "0.0E+00")
    If worstB > worst Then worst = worstB
    If worstB > CHK_TOL Then nBad = nBad + 1
    Note mc, wr, "Stored cells compared after the run", CStr(nCells)
    Note mc, wr, "Cells differing by more than " & Format(CHK_TOL, "0E+00") & " (relative)", CStr(nBad)
    Note mc, wr, "Largest relative difference (baseline and batch)", Format(worst, "0.0E+00")
    Note mc, wr, "Finished", Format(Now, "yyyy-mm-dd hh:mm:ss")
    mc.Cells(CHK_FIRST, 1).Value = "Result"
    If nBad = 0 And nMissing = 0 Then
        mc.Cells(CHK_FIRST, 2).Value = "PASS"
    Else
        mc.Cells(CHK_FIRST, 2).Value = "CHECK: " & nBad & " value(s) differ, " & nMissing & " row(s) missing"
    End If
    CheckBatch = worst
End Function

Private Sub Note(ByVal mc As Worksheet, ByRef wr As Long, ByVal item As String, ByVal result As String)
    mc.Cells(wr, 1).Value = item
    mc.Cells(wr, 2).Value = result
    wr = wr + 1
End Sub

Private Function Probe(ByVal kind As String, ByVal arg As String, ByRef msg As String) As Long
    On Error GoTo Failed
    Select Case kind
        Case "mtcol": Probe = MTColumn(CLng(arg))
        Case "mtparam": Probe = MTParamRow(arg)
        Case "mitbase": Probe = MitBaseCol(CLng(arg))
        Case "mitrow": Probe = MitRow(arg)
        Case "outblock": Probe = OutBlockRow(CLng(arg))
        Case "name": Probe = ThisWorkbook.Names(arg).RefersToRange.Row
    End Select
    Exit Function
Failed:
    msg = Err.Description
    Probe = -1
End Function

Private Function OutBlockRow(ByVal scen As Long) As Long
    Dim mo As Worksheet, r As Long
    Set mo = ThisWorkbook.Worksheets(SH_OUT)
    For r = 5 To 2000
        If CStr(mo.Cells(r, 1).Value) = "Scenario block" Then
            If Num(mo.Cells(r, 5).Value) = scen Then
                OutBlockRow = r
                Exit Function
            End If
        End If
    Next r
    Err.Raise vbObjectError + 6, , "No MTOutputs block for scenario " & scen
End Function

Private Function ReadStored(ByRef ids() As Double, ByRef stems() As String, ByRef vals() As Double) As Long
    Dim sr As Worksheet, n As Long, r As Long, j As Long
    UpgradeStoredCodes                                    ' v7.2: v7.1 stems renamed first
    Set sr = ThisWorkbook.Worksheets(SH_SR)
    n = FirstFreeRow() - SR_FIRST
    ReDim ids(1 To n + 1)
    ReDim stems(1 To n + 1)
    ReDim vals(1 To n + 1, 1 To NYEARS)
    For r = 1 To n
        ids(r) = Num(sr.Cells(SR_FIRST + r - 1, 1).Value)
        stems(r) = CStr(sr.Cells(SR_FIRST + r - 1, 3).Value)
        For j = 1 To NYEARS
            vals(r, j) = Num(sr.Cells(SR_FIRST + r - 1, SR_COL_Y0 + j - 1).Value)
        Next j
    Next r
    ReadStored = n
End Function

Private Function RelDiff(ByVal a As Double, ByVal b As Double) As Double
    Dim den As Double
    den = Abs(b)
    If den < 1 Then den = 1
    RelDiff = Abs(a - b) / den
End Function

Private Function HostName() As String
    On Error GoTo Failed
    HostName = Application.Name & " " & Application.Version
    Exit Function
Failed:
    HostName = "unknown host"
End Function
