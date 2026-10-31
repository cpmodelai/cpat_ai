Attribute VB_Name = "CPATMaster"
Option Explicit
'==========================================================================
' CPAT-AI Master workbook (module file CPATMaster.bas): the only macros of CPAT-AI (v1.2.0, user 2026-10-31).
' The module workbooks (mitigation, distribution, air pollution) have no macros; this workbook opens them, writes
' to them and reads from them. Untested in Excel at release: see excel_ai/core/NORMS.md 9.7.
'
' Public macros (buttons on UserGuide; Alt+F8):
'   ActivateAll, ActivateMitigation, ActivateDistribution, ActivateAirPollution
'                         open the module's latest .xlsx (the local repository copy, else the GitHub link of the
'                         module table), copy the last shipped year's formulas across to the last model year on the
'                         sheets listed in the table (FillRight), write tab FromMaster, recalculate fully, and save
'                         it as <name>_latest.xlsb next to this workbook (active_workbooks); the workbook stays open.
'   UpdateDataTables      refreshes the linked data tabs of the activated mitigation workbook from the data source
'                         chosen on tab Settings (Power Query; rows of the country, or every country), then saves it.
'   UpdateDistributionFromMitigation
'                         copies section 19a (ExportDistn) of the activated mitigation workbook into FromMitigation
'                         of the activated distribution workbook, recalculates and saves it.
'   StoreLiveScenarios    copies every scenario group of MTOutputs of the activated mitigation workbook into the
'                         next free slots of StoredScenarios (values).
'   RunStoredScenarios    batch run: the baseline (if not stored), then every definition of MTInputs with Run? =
'                         Yes, through the live column K of the mitigation workbook (ETS goal seek where needed);
'                         each result stored in a slot of StoredScenarios.
'   ClearStoredScenarios  empties every slot but the first (the baseline).
'==========================================================================

' @@CONSTANTS@@

Private ModWb As Workbook                         ' the module workbook a macro works on

Public Function MasterVersion() As String
    ' the version of this workbook (also a compile test: LibreOffice runs it in the build check)
    MasterVersion = MASTER_VERSION
End Function

'---------------------------------------------------------------- activation
Public Sub ActivateAll()
    Dim r As Long, n As Long, msg As String
    For r = 1 To ModTable().Rows.Count
        If Len(CStr(ModTable().Cells(r, 1).Value)) > 0 Then
            If ActivateRow(r, msg) Then n = n + 1
        End If
    Next r
    MsgBox n & " module(s) activated (saved as .xlsb in " & ThisWorkbook.Path & ")." & msg, vbInformation, "CPAT Master"
End Sub

Public Sub ActivateMitigation()
    ActivateOne "Mitigation"
End Sub

Public Sub ActivateDistribution()
    ActivateOne "Distribution"
End Sub

Public Sub ActivateAirPollution()
    ActivateOne "Air pollution"
End Sub

Private Sub ActivateOne(ByVal key As String)
    Dim msg As String, r As Long
    r = ModRow(key)
    If ActivateRow(r, msg) Then
        MsgBox key & " activated: " & ModTable().Cells(r, COL_ACT).Value & msg, vbInformation, "CPAT Master"
    Else
        MsgBox key & ": not activated." & msg, vbExclamation, "CPAT Master"
    End If
End Sub

Private Function ActivateRow(ByVal r As Long, ByRef msg As String) As Boolean
    Dim src As String, dst As String, w As Workbook, calc As Long, sec As Long, s As Variant
    If r = 0 Then Exit Function
    src = SourcePath(r)
    If Len(src) = 0 Then
        msg = msg & vbLf & ModTable().Cells(r, 1).Value & ": no local file and no link"
        Exit Function
    End If
    dst = ThisWorkbook.Path & Application.PathSeparator & CStr(ModTable().Cells(r, COL_ACT).Value)
    CloseByName CStr(ModTable().Cells(r, COL_ACT).Value)
    calc = Application.Calculation
    sec = Application.AutomationSecurity
    On Error GoTo fail
    Application.ScreenUpdating = False
    Application.AutomationSecurity = AUTOSEC_FORCE_DISABLE
    Set w = Application.Workbooks.Open(Filename:=src, UpdateLinks:=0, ReadOnly:=True)
    Application.AutomationSecurity = sec
    Application.Calculation = xlCalculationManual
    For Each s In Split(CStr(ModTable().Cells(r, COL_FILL).Value), ",")
        If Len(Trim(CStr(s))) > 0 Then FillAcross w.Worksheets(Trim(CStr(s)))
    Next s
    WriteFromMaster w, "FMVersion", MASTER_VERSION
    WriteFromMaster w, "FMActivated", "activated " & Format(Now, "yyyy-mm-dd hh:nn") & " from " & src
    Application.CalculateFull
    Application.CalculateFull                    ' a second pass: NORMS 3i.2
    Application.DisplayAlerts = False
    w.SaveAs Filename:=dst, FileFormat:=XL_XLSB
    Application.DisplayAlerts = True
    ModTable().Cells(r, COL_LAST).Value = Format(Now, "yyyy-mm-dd hh:nn")
    Application.Calculation = calc
    Application.ScreenUpdating = True
    ActivateRow = True
    Exit Function
fail:
    msg = msg & vbLf & ModTable().Cells(r, 1).Value & ": " & Err.Description
    Application.AutomationSecurity = sec
    Application.DisplayAlerts = True
    Application.Calculation = calc
    Application.ScreenUpdating = True
End Function

Private Sub FillAcross(ByVal ws As Worksheet)
    ' every column whose row 1 is the last shipped year starts a scenario group's fill: the column is copied across to
    ' the last model year, every row (Excel's FillRight shifts the references, as dragging does)
    Dim c As Long, lastC As Long, lastR As Long, v As Variant, cols As New Collection, k As Variant
    lastR = ws.UsedRange.Row + ws.UsedRange.Rows.Count - 1
    lastC = ws.UsedRange.Column + ws.UsedRange.Columns.Count - 1
    For c = 1 To lastC
        v = ws.Cells(1, c).Value
        If Not IsError(v) Then
            If VarType(v) <> vbString And Not IsEmpty(v) Then
                If IsNumeric(v) Then
                    If CLng(v) = SHIP_LAST Then cols.Add c
                End If
            End If
        End If
    Next c
    For Each k In cols
        ws.Range(ws.Cells(1, CLng(k)), ws.Cells(lastR, CLng(k) + LAST_YEAR - SHIP_LAST)).FillRight
    Next k
End Sub

Private Function SourcePath(ByVal r As Long) As String
    ' the module's .xlsx in the local repository (path relative to excel_ai, this workbook in excel_ai/active_workbooks),
    ' else its GitHub link
    Dim p As String, sep As String
    sep = Application.PathSeparator
    p = ThisWorkbook.Path & sep & ".." & sep & Replace(Replace(CStr(ModTable().Cells(r, COL_FILE).Value), "/", sep), "\", sep)
    If Left(ThisWorkbook.Path, 4) <> "http" Then
        If Len(Dir(p)) > 0 Then SourcePath = p: Exit Function
    End If
    SourcePath = CStr(ModTable().Cells(r, COL_URL).Value)
End Function

Private Function OpenActive(ByVal key As String) As Workbook
    ' the activated module: open already, else opened from active_workbooks (read-write); Nothing if not activated
    Dim nm As String, w As Workbook, p As String, sec As Long
    nm = CStr(ModTable().Cells(ModRow(key), COL_ACT).Value)
    For Each w In Application.Workbooks
        If LCase(w.Name) = LCase(nm) Then Set OpenActive = w: Exit Function
    Next w
    p = ThisWorkbook.Path & Application.PathSeparator & nm
    If Len(Dir(p)) = 0 Then Exit Function
    sec = Application.AutomationSecurity
    Application.AutomationSecurity = AUTOSEC_FORCE_DISABLE
    Set OpenActive = Application.Workbooks.Open(Filename:=p, UpdateLinks:=0)
    Application.AutomationSecurity = sec
End Function

Private Sub CloseByName(ByVal nm As String)
    Dim w As Workbook
    For Each w In Application.Workbooks
        If LCase(w.Name) = LCase(nm) Then w.Close SaveChanges:=False: Exit Sub
    Next w
End Sub

Private Sub WriteFromMaster(ByVal w As Workbook, ByVal nm As String, ByVal v As Variant)
    On Error Resume Next                          ' a module without tab FromMaster (air pollution scaffold)
    w.Names(nm).RefersToRange.Value = v
    On Error GoTo 0
End Sub

Private Function ModTable() As Range
    Set ModTable = ThisWorkbook.Names("ModTable").RefersToRange
End Function

Private Function ModRow(ByVal key As String) As Long
    Dim r As Long
    For r = 1 To ModTable().Rows.Count
        If LCase(CStr(ModTable().Cells(r, 1).Value)) = LCase(key) Then ModRow = r: Exit Function
    Next r
End Function

Private Function NeedActive(ByVal key As String) As Boolean
    Set ModWb = OpenActive(key)
    If ModWb Is Nothing Then
        MsgBox key & " is not activated yet: click Activate first.", vbExclamation, "CPAT Master"
    Else
        NeedActive = True
    End If
End Function

'---------------------------------------------------------------- data tables (v0.6.5; v1.2.0: from the Master)
Public Sub UpdateDataTables()
    Dim src As String, kind As String, loc As String, srcExpr As String, iso As String, allRows As Boolean
    Dim lt As Range, r As Long, calc As Long, n As Long, msg As String, t0 As Double, rowsOf As String
    If Not NeedActive("Mitigation") Then Exit Sub
    src = CStr(ThisWorkbook.Names("DataSource").RefersToRange.Value)
    allRows = LCase(Left(CStr(ThisWorkbook.Names("DataRows").RefersToRange.Value), 3)) = "all"
    If src Like "Embedded*" Then
        MsgBox "Data source is '" & src & "': the shipped data are used, nothing to update." & vbLf & _
               "Choose another source on tab Settings first.", vbInformation, "CPAT data"
        Exit Sub
    End If
    If Not SourceOf(src, kind, loc) Then
        MsgBox "Data source '" & src & "' is not in the source table on tab Settings.", vbExclamation, "CPAT data"
        Exit Sub
    End If
    If kind = "file" Then
        If Len(loc) = 0 Then loc = FindLocalData()
        If Len(loc) = 0 Then Exit Sub
        srcExpr = "File.Contents(""" & loc & """)"
    Else
        If Len(loc) = 0 Then
            MsgBox "Data source '" & src & "' has no address: type the URL of the data workbook (" & DATA_FILE & _
                   ") in its row of the source table on tab Settings.", vbExclamation, "CPAT data"
            Exit Sub
        End If
        If InStr(loc, "/:x:/") > 0 And InStr(loc, "download=1") = 0 Then
            loc = loc & IIf(InStr(loc, "?") > 0, "&", "?") & "download=1"
        End If
        srcExpr = "Web.Contents(""" & loc & """)"
    End If
    iso = UCase(CStr(ModWb.Names("CtryCode").RefersToRange.Value))
    calc = Application.Calculation
    Application.Calculation = xlCalculationManual
    Application.ScreenUpdating = False
    t0 = Timer
    On Error GoTo fail
    Set lt = ModWb.Names("DataLinkTable").RefersToRange
    For r = 1 To lt.Rows.Count
        If Len(CStr(lt.Cells(r, 1).Value)) > 0 Then
            rowsOf = IIf(allRows, "all", CStr(lt.Cells(r, 5).Value))
            n = RefreshLink(CStr(lt.Cells(r, 1).Value), CStr(lt.Cells(r, 2).Value), CStr(lt.Cells(r, 3).Value), _
                            CLng(lt.Cells(r, 4).Value), rowsOf, srcExpr, iso, msg)
            lt.Cells(r, 6).Value = n & IIf(LCase(rowsOf) = "all", " rows (all), ", " rows of " & iso & ", ") & src & _
                                   ", " & Format(Now, "yyyy-mm-dd hh:nn")
            If n = 0 Then msg = msg & vbLf & "  " & lt.Cells(r, 1).Value & ": no rows (shipped data kept)"
        End If
    Next r
    WriteFromMaster ModWb, "FMSource", src
    WriteFromMaster ModWb, "FMRows", IIf(allRows, "All countries", "Country (" & iso & ")")
    WriteFromMaster ModWb, "FMPath", loc
    ModWb.Names("DataUsed").RefersToRange.Value = loc
    ModWb.Names("DataSavedIn").RefersToRange.Value = ModWb.Path
    ModWb.Names("DataLastUpdate").RefersToRange.Value = src & " (" & IIf(allRows, "all countries", iso) & "), " & _
                                                    Format(Now, "yyyy-mm-dd hh:nn")
    Application.CalculateFull
    ModWb.Save
    Application.Calculation = calc
    Application.ScreenUpdating = True
    MsgBox "Linked data tables of " & ModWb.Name & " updated from '" & src & "' in " & Format(Timer - t0, "0.0") & _
           " s and saved." & IIf(Len(msg) > 0, vbLf & "Warning:" & msg, ""), vbInformation, "CPAT data"
    Exit Sub
fail:
    Application.Calculation = calc
    Application.ScreenUpdating = True
    MsgBox "Update failed: " & Err.Description & vbLf & vbLf & _
           "SharePoint: sign in with 'Organizational account' when asked; if a Share link fails, open the data " & _
           "file in Excel desktop, File > Info > Copy path, and paste that path in the source table on tab Settings." & _
           vbLf & "Local file: check the path in the source table (blank = searched in the repository).", _
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
    ' the repository layout: <repo>\data\Public01\legacy_xlsx\CPAT_LegacyData.xlsx; the workbook in excel_ai\ or
    ' excel_ai\mitigation\, or the data file next to the workbook
    Dim cands As Variant, c As Variant, p As String, f As Variant
    p = ThisWorkbook.Path & Application.PathSeparator & ".."
    If Left(p, 4) <> "http" Then
        cands = Array(p & "\" & DATA_FILE, p & "\data\Public01\legacy_xlsx\" & DATA_FILE, _
                      p & "\..\data\Public01\legacy_xlsx\" & DATA_FILE, p & "\..\..\data\Public01\legacy_xlsx\" & DATA_FILE, _
                      p & "\..\..\..\data\Public01\legacy_xlsx\" & DATA_FILE)
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
    ' v0.7.1: the query loads into a staging sheet; its columns are copied to the tab by the names in the tab's own
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
    Set q = ModWb.Queries(qn)
    On Error GoTo 0
    If q Is Nothing Then
        ModWb.Queries.Add qn, m
    Else
        q.Formula = m
    End If
    Set ws = ModWb.Worksheets(tabName)
    hadAlerts = Application.DisplayAlerts
    Application.DisplayAlerts = False
    On Error Resume Next                        ' a staging sheet left by an interrupted update
    ModWb.Worksheets("zStage").Delete
    On Error GoTo 0
    Application.DisplayAlerts = hadAlerts
    Set st =ModWb.Worksheets.Add(After:=ModWb.Worksheets(ModWb.Worksheets.Count))
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
    For Each cn In ModWb.Connections
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

'---------------------------------------------------------------- distribution from mitigation (was CPATDistribution.bas)
Public Sub UpdateDistributionFromMitigation()
    Dim wbM As Workbook, wbD As Workbook, rng As Range, ws As Worksheet, fm As Worksheet, v As Variant
    Dim nr As Long, lastCol As Long, r As Long, c As Long, calc As Long, bad As String, outv() As Variant
    If Not NeedActive("Mitigation") Then Exit Sub
    Set wbM = ModWb
    If Not NeedActive("Distribution") Then Exit Sub
    Set wbD = ModWb
    Set rng = wbM.Names(EXPORT_NAME).RefersToRange
    Set ws = rng.Worksheet
    Set fm = wbD.Worksheets(SH_FM)
    calc = Application.Calculation
    Application.Calculation = xlCalculationManual
    Application.ScreenUpdating = False
    On Error GoTo fail
    lastCol = ws.UsedRange.Column + ws.UsedRange.Columns.Count - 1
    If lastCol > FM_COL_LAST Then lastCol = FM_COL_LAST
    If lastCol < FM_COL_FIRST Then lastCol = FM_COL_FIRST
    nr = rng.Rows.Count
    v = ws.Range(ws.Cells(rng.Row, 1), ws.Cells(rng.Row + nr - 1, lastCol)).Value
    If nr - 2 <> FM_LAST - FM_FIRST + 1 Then
        bad = (nr - 2) & " rows in " & EXPORT_NAME & ", " & (FM_LAST - FM_FIRST + 1) & " in " & SH_FM
    Else
        For r = 3 To nr
            If Trim(CStr(v(r, 1))) <> Trim(CStr(fm.Cells(FM_FIRST + r - 3, 1).Value)) Then
                bad = bad & IIf(Len(bad) > 0, ", ", "") & "row " & (FM_FIRST + r - 3)
            End If
        Next r
    End If
    If Len(bad) > 0 Then Err.Raise 1004, , "the export of the mitigation workbook does not match " & SH_FM & _
                                          " (different versions?): " & bad
    ReDim outv(1 To 1, 1 To FM_COL_LAST - FM_COL_FIRST + 1)
    For r = 1 To nr
        For c = FM_COL_FIRST To FM_COL_LAST
            If c <= lastCol Then outv(1, c - FM_COL_FIRST + 1) = v(r, c) Else outv(1, c - FM_COL_FIRST + 1) = Empty
        Next c
        fm.Cells(FmRow(r), FM_COL_FIRST).Resize(1, FM_COL_LAST - FM_COL_FIRST + 1).Value = outv
    Next r
    wbD.Names("MitUsed").RefersToRange.Value = wbM.FullName
    wbD.Names("MitLastUpdate").RefersToRange.Value = wbM.Name & ", copied " & Format(Now, "yyyy-mm-dd hh:nn")
    Application.CalculateFull
    wbD.Save
    Application.Calculation = calc
    Application.ScreenUpdating = True
    MsgBox "FromMitigation of " & wbD.Name & " updated from " & wbM.Name & ", recalculated and saved.", _
           vbInformation, "CPAT Master"
    Exit Sub
fail:
    Application.Calculation = calc
    Application.ScreenUpdating = True
    MsgBox "Update failed: " & Err.Description, vbExclamation, "CPAT Master"
End Sub

Private Function FmRow(ByVal r As Long) As Long
    ' row r of ExportDistn: 1 = years (FromMitigation row 1), 2 = scenario numbers (row 5), then the data rows
    If r = 1 Then
        FmRow = 1
    ElseIf r = 2 Then
        FmRow = 5
    Else
        FmRow = FM_FIRST + r - 3
    End If
End Function

'---------------------------------------------------------------- stored scenarios (values; were StoredOutputs)
Public Sub StoreLiveScenarios()
    Dim mo As Worksheet, c As Long, n As Long, last As Long
    If Not NeedActive("Mitigation") Then Exit Sub
    Recalc
    Set mo = ModWb.Worksheets(SH_OUT)
    last = mo.UsedRange.Column + mo.UsedRange.Columns.Count - 1
    For c = OUT_COL_G0 To last Step GW
        If Num(mo.Cells(OUT_ROW_SCEN, c).Value) > 0 Then
            If StoreGroup(CLng(mo.Cells(OUT_ROW_SCEN, c).Value), "") = 0 Then Exit For
            n = n + 1
        End If
    Next c
    MsgBox n & " live scenario(s) of " & ModWb.Name & " stored in " & SH_SS & ".", vbInformation, "CPAT Master"
End Sub

Public Sub RunStoredScenarios()
    Dim n As Long
    If Not NeedActive("Mitigation") Then Exit Sub
    n = RunAll()
    MsgBox n & " scenario definition(s) of " & ModWb.Name & " run and stored in " & SH_SS & _
           " (the mitigation workbook is not saved: its live column is restored).", vbInformation, "CPAT Master"
End Sub

Public Sub ClearStoredScenarios()
    Dim ss As Worksheet, k As Long
    If MsgBox("Empty every stored slot except the first (the baseline)?", vbYesNo + vbQuestion, "CPAT Master") <> vbYes _
        Then Exit Sub
    Set ss = ThisWorkbook.Worksheets(SH_SS)
    For k = 2 To SS_SLOTS
        ss.Range(ss.Cells(SS_ROW_NAME, SlotCol(k)), ss.Cells(SS_LAST, SlotCol(k) + NYEARS)).ClearContents
    Next k
End Sub

Private Function StoreGroup(ByVal scen As Long, ByVal nm As String, Optional ByVal id As Long = 0) As Long
    ' the MTOutputs group of scenario scen (module ModWb) into the slot of the ID (replaced), else the next free slot;
    ' the rows of StoredScenarios are those of MTOutputs (checked on the code stems). Returns the slot, 0 if full.
    Dim mo As Worksheet, ss As Worksheet, c0 As Long, k As Long, s0 As Long, v As Variant, r As Long
    Set mo = ModWb.Worksheets(SH_OUT)
    Set ss = ThisWorkbook.Worksheets(SH_SS)
    If id = 0 Then id = scen
    For c0 = OUT_COL_G0 To OUT_COL_G0 + 40 * GW Step GW
        If Num(mo.Cells(OUT_ROW_SCEN, c0).Value) = scen Then Exit For
    Next c0
    If Num(mo.Cells(OUT_ROW_SCEN, c0).Value) <> scen Then Err.Raise vbObjectError + 6, , "No MTOutputs group " & scen
    For r = SS_FIRST To SS_LAST Step 50
        If CStr(mo.Cells(r, 1).Value) <> CStr(ss.Cells(r, 1).Value) Then _
            Err.Raise vbObjectError + 7, , "MTOutputs row " & r & " is not the row of " & SH_SS & " (other version?)"
    Next r
    k = SlotOfId(id)
    If k = 0 Then k = FreeSlot()
    If k = 0 Then
        MsgBox "No free slot in " & SH_SS & ": clear one first.", vbExclamation, "CPAT Master"
        Exit Function
    End If
    s0 = SlotCol(k)
    If Len(nm) = 0 Then nm = CStr(mo.Cells(OUT_ROW_NAME, c0 + 1).Value)
    v = mo.Range(mo.Cells(SS_FIRST, c0), mo.Cells(SS_LAST, c0 + NYEARS)).Value
    ss.Range(ss.Cells(SS_FIRST, s0), ss.Cells(SS_LAST, s0 + NYEARS)).Value = v
    ss.Range(ss.Cells(SS_ROW_ID, s0), ss.Cells(SS_ROW_ID, s0 + NYEARS)).Value = id
    ss.Cells(SS_ROW_NAME, s0 + 1).Value = nm
    ss.Cells(SS_ROW_META, s0 + 1).Value = "stored " & Format(Now, "yyyy-mm-dd hh:nn") & " from " & ModWb.Name & ", " & _
                                           UCase(CStr(ModWb.Names("CtryCode").RefersToRange.Value))
    StoreGroup = k
End Function

Private Function SlotCol(ByVal k As Long) As Long
    SlotCol = SS_COL_G0 + (k - 1) * GW
End Function

Private Function SlotOfId(ByVal id As Long) As Long
    Dim k As Long
    For k = 1 To SS_SLOTS
        If Num(ThisWorkbook.Worksheets(SH_SS).Cells(SS_ROW_ID, SlotCol(k)).Value) = id Then SlotOfId = k: Exit Function
    Next k
End Function

Private Function FreeSlot() As Long
    Dim k As Long
    For k = 1 To SS_SLOTS
        If IsEmpty(ThisWorkbook.Worksheets(SH_SS).Cells(SS_ROW_ID, SlotCol(k)).Value) Then FreeSlot = k: Exit Function
    Next k
End Function

Private Sub Recalc()
    ' recalculate twice: in Excel the second pass costs nothing; LibreOffice needs it (NORMS 3i.2)
    Application.Calculate
    Application.Calculate
End Sub

'---------------------------------------------------------------- batch run on the mitigation workbook ModWb
Private Function RunAll() As Long
    Dim mt As Worksheet, liveCol As Long, c As Long, r As Long, n As Long
    Dim savedVal(1 To MT_LAST) As Variant, savedIsF(1 To MT_LAST) As Boolean
    Dim ovr As Long, ovrBase As Long, savedOvr(1 To NYEARS) As Variant, j As Long
    Set mt = ModWb.Worksheets(SH_MT)
    liveCol = MTColumn(LIVE_SCEN)
    For r = 1 To MT_LAST                                  ' save the live column (formulas and values)
        savedIsF(r) = mt.Cells(r, liveCol).HasFormula
        If savedIsF(r) Then savedVal(r) = mt.Cells(r, liveCol).Formula Else savedVal(r) = mt.Cells(r, liveCol).Value
    Next r
    ovr = MitRow("ets.ovr")
    ovrBase = MitBaseCol(LIVE_SCEN)
    For j = 1 To NYEARS
        savedOvr(j) = ModWb.Worksheets(SH_MIT).Cells(ovr, ovrBase + j - 1).Value
    Next j
    Dim calcWas As Long
    calcWas = Application.Calculation                     ' v0.6.6: restored at the end (the workbook ships manual)
    On Error Resume Next
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    On Error GoTo 0
    Recalc
    If SlotOfId(BASE_SCEN) = 0 Then StoreGroup BASE_SCEN, ""
    c = liveCol + 1
    Do While Not IsEmpty(mt.Cells(MT_ROW_NUM, c).Value)
        If UCase(Left(Trim(CStr(mt.Cells(MT_ROW_RUN, c).Value)), 1)) = "Y" Then
            For r = MT_FIRST To MT_LAST
                If r <> MT_ROW_ID And r <> MT_ROW_IDNAME Then mt.Cells(r, liveCol).Value = mt.Cells(r, c).Value
            Next r
            mt.Cells(MT_ROW_NAME, liveCol).Value = mt.Cells(MT_ROW_NAME, c).Value
            For j = 1 To NYEARS
                ModWb.Worksheets(SH_MIT).Cells(ovr, ovrBase + j - 1).ClearContents
            Next j
            Recalc
            If NeedsETS(liveCol) Then SolveETS
            StoreGroup LIVE_SCEN, CStr(mt.Cells(MT_ROW_NAME, c).Value), CLng(mt.Cells(MT_ROW_NUM, c).Value)
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
            ModWb.Worksheets(SH_MIT).Cells(ovr, ovrBase + j - 1).ClearContents
        Else
            ModWb.Worksheets(SH_MIT).Cells(ovr, ovrBase + j - 1).Value = savedOvr(j)
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
    maxIt = CLng(Num(NamedValue("ETSMaxIterations")))     ' v0.5.2: Manual inputs E10:E12 (legacy addresses)
    If maxIt < 1 Then maxIt = ETS_MAXITER
    tol = Num(NamedValue("ETSErrorTolerance"))
    If tol <= 0 Then tol = ETS_TOL
    fresh = LCase(Left(CStr(NamedValue("ETSStartFreshContinue")), 5)) = "start"
    Set mit = ModWb.Worksheets(SH_MIT)
    Set mt = ModWb.Worksheets(SH_MT)
    liveCol = MTColumn(LIVE_SCEN)
    mt.Cells(MTParamRow("ETSPriceOverride"), liveCol).Value = "Yes"
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
    NamedValue = ModWb.Names(nm).RefersToRange.Value  ' v0.5.2: a single-cell workbook name
End Function

Private Function LogStep(ByVal pc As Double, ByVal pr As Double, ByVal alpha As Double) As Double
    If pc <= 0 Or pr <= 0 Then
        LogStep = pc + alpha * (pr - pc)
        If LogStep < 0 Then LogStep = 0
    Else
        LogStep = pc * (pr / pc) ^ alpha
    End If
End Function

'---------------------------------------------------------------- lookups in the mitigation workbook ModWb
Private Function MTColumn(ByVal scen As Long) As Long
    Dim c As Long
    For c = MT_COL_FIRST To MT_COL_FIRST + 200
        If Num(ModWb.Worksheets(SH_MT).Cells(MT_ROW_NUM, c).Value) = scen Then
            MTColumn = c
            Exit Function
        End If
    Next c
    Err.Raise vbObjectError + 2, , "Scenario " & scen & " not found in MTInputs row 5"
End Function

Private Function MTParamRow(ByVal nm As String) As Long
    Dim r As Long
    For r = MT_FIRST To MT_LAST
        If CStr(ModWb.Worksheets(SH_MT).Cells(r, MT_COL_PARAM).Value) = nm Then
            MTParamRow = r
            Exit Function
        End If
    Next r
    Err.Raise vbObjectError + 3, , "Parameter " & nm & " not found in MTInputs column H"
End Function

Private Function NeedsETS(ByVal liveCol As Long) As Boolean
    Dim mt As Worksheet
    Set mt = ModWb.Worksheets(SH_MT)
    NeedsETS = UCase(Left(CStr(mt.Cells(MTParamRow("NewETS"), liveCol).Value), 3)) = "YES" And _
               UCase(Left(CStr(mt.Cells(MTParamRow("ETSPriceOverride"), liveCol).Value), 3)) <> "YES"
End Function

Private Function MitRow(ByVal code As String) As Long
    Dim r As Long
    For r = 1 To MIT_MAX_ROW
        If CStr(ModWb.Worksheets(SH_MIT).Cells(r, 1).Value) = code Then
            MitRow = r
            Exit Function
        End If
    Next r
    Err.Raise vbObjectError + 4, , "Row " & code & " not found in Mitigation column A"
End Function

Private Function MitBaseCol(ByVal scen As Long) As Long
    Dim c As Long
    For c = MIT_COL_FIRST To MIT_COL_FIRST + 2000
        If Num(ModWb.Worksheets(SH_MIT).Cells(MIT_ROW_SCEN, c).Value) = scen Then
            MitBaseCol = c + 1                            ' code column + 1 = base year
            Exit Function
        End If
    Next c
    Err.Raise vbObjectError + 5, , "Scenario group " & scen & " not found in Mitigation row 5"
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
