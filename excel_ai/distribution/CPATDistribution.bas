Attribute VB_Name = "CPATDistribution"
Option Explicit
'==========================================================================
' CPAT-AI-Distribution-Prototype (module file CPATDistribution.bas): the link to the mitigation prototype.
'
' The distribution module reads Mitigation only through its tab FromMitigation, a copy of section 19a
' (defined name ExportDistn) of the mitigation workbook, in the Mitigation column layout.
'
' Public macros (Alt+F8):
'   UpdateFromMitigation  copies the values of ExportDistn from the mitigation workbook named on Cover
'                         (MitSource; a name alone is looked for next to this workbook, in permalink_countryeditable\ and permalink\, then the same one folder up)
'                         into FromMitigation, after checking that the rows are the same variables. If the
'                         mitigation workbook is open, its current values are used (recalculate it first);
'                         otherwise it is opened read-only, without macros or recalculation, and closed.
'                         Then recalculates this workbook.
'   RecalculateNow        recalculates this workbook (it ships with its values, in manual calculation).
'   ToggleRecalculation   switches automatic calculation on or off.
'==========================================================================

Private Const SH_FM As String = "FromMitigation"
Private Const EXPORT_NAME As String = "ExportDistn"
Private Const FM_FIRST As Long = 8            ' first data row of FromMitigation (rows 1 and 5: years, scenario numbers)
Private Const FM_LAST As Long = 35            ' last data row (the builder asserts it)
Private Const FM_COL_FIRST As Long = 11       ' K: code column of scenario group 1
Private Const FM_COL_LAST As Long = 260       ' IZ: last column Distribution can read
Private Const MIT_FILE As String = "CPAT-AI-Mitigation-Prototype_latest.xlsm"
Private Const AUTOSEC_FORCE_DISABLE As Long = 3   ' msoAutomationSecurityForceDisable (Office library not referenced)

'---------------------------------------------------------------- public macros
Public Sub UpdateFromMitigation()
    Dim path As String, wbM As Workbook, opened As Boolean, rng As Range, ws As Worksheet, fm As Worksheet
    Dim v As Variant, nr As Long, lastCol As Long, r As Long, c As Long, calc As Long, sec As Long
    Dim bad As String, stamp As String, t0 As Double, outv() As Variant
    path = MitPath()
    If Len(path) = 0 Then Exit Sub
    Set fm = ThisWorkbook.Worksheets(SH_FM)
    calc = Application.Calculation
    sec = Application.AutomationSecurity
    Application.Calculation = xlCalculationManual       ' before opening: no recalculation of the mitigation workbook
    Application.ScreenUpdating = False
    t0 = Timer
    On Error GoTo fail
    Set wbM = OpenMitigation(path, opened)
    Set rng = wbM.Names(EXPORT_NAME).RefersToRange
    Set ws = rng.Worksheet
    lastCol = ws.UsedRange.Column + ws.UsedRange.Columns.Count - 1   ' scenario groups pasted after the name was set
    If lastCol > FM_COL_LAST Then lastCol = FM_COL_LAST
    If lastCol < FM_COL_FIRST Then lastCol = FM_COL_FIRST
    nr = rng.Rows.Count
    v = ws.Range(ws.Cells(rng.Row, 1), ws.Cells(rng.Row + nr - 1, lastCol)).Value
    stamp = wbM.Name & " (" & StampOf(wbM, opened) & ")"
    If opened Then wbM.Close SaveChanges:=False
    Set wbM = Nothing
    Application.AutomationSecurity = sec
    If nr - 2 <> FM_LAST - FM_FIRST + 1 Then
        bad = (nr - 2) & " rows in " & EXPORT_NAME & ", " & (FM_LAST - FM_FIRST + 1) & " in " & SH_FM
    Else
        For r = 3 To nr
            If Trim(CStr(v(r, 1))) <> Trim(CStr(fm.Cells(FM_FIRST + r - 3, 1).Value)) Then
                bad = bad & IIf(Len(bad) > 0, ", ", "") & "row " & (FM_FIRST + r - 3) & ": " & _
                      CStr(v(r, 1)) & " <> " & CStr(fm.Cells(FM_FIRST + r - 3, 1).Value)
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
    ThisWorkbook.Names("MitUsed").RefersToRange.Value = path
    ThisWorkbook.Names("MitLastUpdate").RefersToRange.Value = stamp & ", copied " & Format(Now, "yyyy-mm-dd hh:nn")
    Application.ScreenUpdating = True
    Application.CalculateFull
    Application.Calculation = calc
    MsgBox "FromMitigation updated from " & stamp & " and recalculated in " & Format(Timer - t0, "0.0") & " s.", _
           vbInformation, "CPAT distribution"
    Exit Sub
fail:
    Application.AutomationSecurity = sec
    If opened And Not wbM Is Nothing Then wbM.Close SaveChanges:=False
    Application.Calculation = calc
    Application.ScreenUpdating = True
    MsgBox "Update failed: " & Err.Description & vbLf & vbLf & "Check the mitigation workbook on Cover " & _
           "(a name alone is looked for next to this workbook, in permalink_countryeditable\ and permalink\, then one folder up).", vbExclamation, "CPAT distribution"
End Sub

Public Sub CalculationOn()
    Application.Calculation = xlCalculationAutomatic
    Application.CalculateFull
End Sub

Public Sub CalculationOff()
    Application.Calculation = xlCalculationManual
End Sub

Public Sub RecalculateNow()
    Dim t As Double
    t = Timer
    Application.StatusBar = "Recalculating CPAT distribution..."
    Application.CalculateFull
    Application.StatusBar = False
    MsgBox "Recalculated in " & Format(Timer - t, "0.0") & " seconds.", vbInformation, "CPAT distribution"
End Sub

Public Sub ToggleRecalculation()
    If Application.Calculation = xlCalculationManual Then
        Application.Calculation = xlCalculationAutomatic
        MsgBox "Recalculation is ON (automatic). Every change recalculates the workbook." & vbCrLf & _
               "Note: Excel applies this to every open workbook.", vbInformation, "CPAT distribution"
    Else
        Application.Calculation = xlCalculationManual
        MsgBox "Recalculation is OFF (manual). Use 'Recalculate now' to update the results.", vbInformation, _
               "CPAT distribution"
    End If
End Sub

'---------------------------------------------------------------- helpers
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

Private Function MitPath() As String
    ' the mitigation workbook of Cover (MitSource): a full path or a web address as it is; a name alone next to this
    ' workbook, in permalink_countryeditable\ or permalink\ next to it, or the same one folder up (v0.1.1: the mitigation
    ' prototype's permalink copy is excel_ai\permalink\; release copies sit in excel_ai\releases\); not found: ask
    Dim s As String, cands As Variant, c As Variant, f As Variant
    s = Trim(CStr(ThisWorkbook.Names("MitSource").RefersToRange.Value))
    If Len(s) = 0 Then s = MIT_FILE
    If LCase(Left(s, 4)) = "http" Then MitPath = s: Exit Function
    If Mid(s, 2, 1) = ":" Or Left(s, 2) = "\\" Or Left(s, 1) = "/" Then
        If Len(Dir(s)) > 0 Then MitPath = s: Exit Function
    ElseIf Left(ThisWorkbook.Path, 4) <> "http" Then
        cands = Array(ThisWorkbook.Path & "\" & s, ThisWorkbook.Path & "\permalink_countryeditable\" & s, _
                      ThisWorkbook.Path & "\permalink\" & s, ThisWorkbook.Path & "\..\" & s, _
                      ThisWorkbook.Path & "\..\permalink_countryeditable\" & s, ThisWorkbook.Path & "\..\permalink\" & s)
        ' v1.0.3: the country-editable copies first (NORMS 9.3), then the permalink copies
        For Each c In cands
            If Len(Dir(CStr(c))) > 0 Then
                MitPath = CreateObject("Scripting.FileSystemObject").GetAbsolutePathName(CStr(c))
                Exit Function
            End If
        Next c
    End If
    f = Application.GetOpenFilename("Excel workbooks (*.xlsm;*.xlsx),*.xlsm;*.xlsx", , _
                                    "Find the mitigation workbook (" & s & ")")
    If VarType(f) = vbString Then MitPath = CStr(f)
End Function

Private Function OpenMitigation(ByVal path As String, ByRef opened As Boolean) As Workbook
    ' an open workbook of that file name is used as it stands; otherwise opened read-only, macros off, links not
    ' updated (the calculation is manual already)
    Dim w As Workbook, nm As String
    nm = Mid(path, InStrRev(Replace(path, "/", "\"), "\") + 1)
    For Each w In Application.Workbooks
        If LCase(w.Name) = LCase(nm) Then
            Set OpenMitigation = w
            opened = False
            Exit Function
        End If
    Next w
    Application.AutomationSecurity = AUTOSEC_FORCE_DISABLE
    Set OpenMitigation = Application.Workbooks.Open(Filename:=path, UpdateLinks:=0, ReadOnly:=True)
    opened = True
End Function

Private Function StampOf(ByVal w As Workbook, ByVal opened As Boolean) As String
    ' the saved time of the file; "open, current values" when the workbook was open already
    If Not opened Then
        StampOf = "open, current values"
        Exit Function
    End If
    On Error Resume Next
    StampOf = "saved " & Format(FileDateTime(w.FullName), "yyyy-mm-dd hh:nn")
    If Err.Number <> 0 Then StampOf = "web file"
    On Error GoTo 0
End Function
