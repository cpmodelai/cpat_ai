Attribute VB_Name = "FixL1"
Option Explicit
'==========================================================================
' Bug-fix harness, example bug L1: services electricity demand grows with the INDUSTRIAL
' multiple after 2023 (legacy CPAT, sheet Mitigation, row "Services (public & private)" of the
' elasticity-based power model, baseline and policy blocks).
'
'   Bug  : 2023 = L x services multiple, 2024 onwards = previous x industrial multiple.
'   Fix  : every year from 2024 = previous x services multiple (same pattern as 2023), so the row
'          is the same R1C1 formula from 2023 to the last year (draggable left to right), and the
'          policy row is a paste of the baseline row (copy-pasteable between the blocks).
'
' Run FixL1_ApplyAndVerify (Alt+F8). It never saves the workbook. Report: sheet FixLog.
' FixL1_Revert puts the two rows back (only in the session that applied the fix).
' Works on the ACTIVE workbook, so it can sit in this workbook or in another one.
'
' Rows are found by their labels (column D) and codes (column C), not by row numbers, so a
' version of CPAT with shifted rows still works; a version whose structure or formulas differ
' stops the run before anything is changed (stage P).
'==========================================================================

Private Const SH_MIT As String = "Mitigation"
Private Const SH_LOG As String = "FixLog"
Private Const LBL_SERV As String = "Overall Multiple, Services"
Private Const LBL_IND As String = "Overall Multiple, Industrial"
Private Const LBL_TOT As String = "Total Demand"
Private Const CODE_SRV As String = "srv"
Private Const YEAR_ROW As Long = 1
Private Const YEAR_FIX As Long = 2024     ' first year of the wrong formula
Private Const COL_CODE As Long = 3        ' C
Private Const COL_LABEL As Long = 4       ' D
Private Const COL_Y0 As Long = 11         ' K = 2021
Private Const SCAN_ROWS As Long = 80      ' search window below the multiples
Private Const TOL As Double = 0.000000001
Private Const TOP_N As Long = 15

Private mWs As Worksheet
Private mLog As Worksheet
Private mLogRow As Long
Private mNFail As Long
Private mNReview As Long
Private mNR As Long, mNC As Long
Private mCFix As Long, mCLast As Long
Private mRowB As Long, mRowP As Long      ' services demand row, baseline and policy block
Private mSvcB As Long, mSvcP As Long      ' services multiple
Private mIndB As Long, mIndP As Long      ' industrial multiple
Private mTotB As Long, mTotP As Long      ' total demand
Private mUndoF(1 To 2) As Variant
Private mErr As String

'---------------------------------------------------------------- public macros

Public Sub FixL1_ApplyAndVerify()
    Dim calcMode As Long, fB As Variant, fA As Variant, vB As Variant, vA As Variant
    Dim stB As String, stP As String, t0 As Double

    t0 = Timer
    Set mLog = Nothing
    mErr = ""
    On Error GoTo Fatal
    Set mWs = ActiveWorkbook.Worksheets(SH_MIT)
    calcMode = Application.Calculation
    Application.ScreenUpdating = False
    Application.EnableEvents = False
    StartLog

    '--- P: preflight: is CPAT what this fix expects?
    If Not Locate() Then GoTo Done
    stB = RowState(mRowB, mIndB, mSvcB)
    stP = RowState(mRowP, mIndP, mSvcP)
    Lg "P5", "State of the services demand row, baseline block (row " & mRowB & ")", IIf(stB = "BUG", "PASS", "FAIL"), _
        "state = " & stB & " (BUG = wrong formula present, FIXED = already fixed, OTHER = formulas differ from the register)"
    Lg "P6", "State of the services demand row, policy block (row " & mRowP & ")", IIf(stP = "BUG", "PASS", "FAIL"), _
        "state = " & stP
    If stB <> "BUG" Or stP <> "BUG" Then
        Lg "P7", "Stop", "FAIL", "Nothing was changed: the bug is not present in the form the register describes. " & _
            "Re-read the rows by hand before fixing."
        GoTo Done
    End If

    '--- S1: snapshot before (full recalculation first, so the values are this Excel's own)
    Application.Calculation = xlCalculationManual
    Application.CalculateFull
    Snap fB, vB
    Lg "S1", "Snapshot before the fix", "INFO", mNR & " rows x " & mNC & " columns of formulas; values from column " & COL_Y0

    '--- F: apply the fix: drag in the baseline block, paste into the policy block
    ApplyFix
    Application.CalculateFull
    Snap fA, vA
    Lg "F1", "Fix applied and recalculated", "INFO", "baseline row " & mRowB & ", policy row " & mRowP & _
        ", columns " & ColName(mCFix) & ":" & ColName(mCLast) & " (" & Format(Timer - t0, "0") & " s so far)"

    '--- T: tests
    TestDrag
    TestCopyPaste
    TestFormulaDiff fB, fA
    TestIndependent vA
    TestUnchangedPast vB, vA
    TestErrors vB, vA
    TestTotals vB, vA
    ReportChanges vB, vA

Done:
    On Error Resume Next
    Application.CutCopyMode = False
    If Not mLog Is Nothing Then
        mLog.Cells(2, 3).Value = IIf(mNFail > 0, "FAIL", IIf(mNReview > 0, "REVIEW", "PASS"))
        mLog.Cells(2, 4).Value = mNFail & " failed, " & mNReview & " to review. The workbook has NOT been saved: " & _
            "if PASS, use Save As with the next version name; if not, close without saving."
        mLog.Columns("A:C").AutoFit
        mLog.Columns("D").ColumnWidth = 110
    End If
    Application.Calculation = calcMode
    Application.EnableEvents = True
    Application.ScreenUpdating = True
    If Not mLog Is Nothing Then
        mLog.Activate
        If Application.Interactive Then MsgBox "Fix L1: " & mLog.Cells(2, 3).Value & vbLf & mLog.Cells(2, 4).Value, vbInformation, "Fix L1"
    ElseIf mErr <> "" Then
        If Application.Interactive Then MsgBox "Fix L1 stopped before any change: " & mErr & vbLf & _
            "Is the active workbook the CPAT file with a sheet named " & SH_MIT & "?", vbExclamation, "Fix L1"
    End If
    Exit Sub
Fatal:
    mNFail = mNFail + 1
    mErr = Err.Number & ": " & Err.Description
    If Not mLog Is Nothing Then
        On Error Resume Next
        Lg "ERR", "Run stopped by a VBA error", "FAIL", Err.Number & ": " & Err.Description
    End If
    Resume Done
End Sub

Public Sub FixL1_Revert()
    Dim i As Long, rr As Variant
    If IsEmpty(mUndoF(1)) Then
        If Application.Interactive Then MsgBox "No fix applied in this session. Close the workbook without saving to discard it.", vbExclamation
        Exit Sub
    End If
    rr = Array(0, mRowB, mRowP)
    For i = 1 To 2
        mWs.Range(mWs.Cells(rr(i), mCFix), mWs.Cells(rr(i), mCLast)).FormulaR1C1 = mUndoF(i)
    Next i
    Application.CalculateFull
    If Application.Interactive Then MsgBox "Rows " & mRowB & " and " & mRowP & " restored to the formulas they had before the fix.", vbInformation
End Sub

'---------------------------------------------------------------- stage P: locating rows

Private Function Locate() As Boolean
    Dim lab As Variant, i As Long, nS As Long, nI As Long, s As String
    Dim nmB As Long, nmP As Long, okNames As Boolean, v As Variant

    mNR = mWs.UsedRange.Row + mWs.UsedRange.Rows.Count - 1
    mNC = mWs.UsedRange.Column + mWs.UsedRange.Columns.Count - 1
    lab = mWs.Range(mWs.Cells(1, COL_LABEL), mWs.Cells(mNR, COL_LABEL)).Value2
    For i = 1 To mNR
        If VarType(lab(i, 1)) = vbString Then
            s = LCase$(Trim$(lab(i, 1)))
            If s = LCase$(LBL_SERV) Then
                nS = nS + 1
                If nS = 1 Then mSvcB = i
                If nS = 2 Then mSvcP = i
            ElseIf s = LCase$(LBL_IND) Then
                nI = nI + 1
                If nI = 1 Then mIndB = i
                If nI = 2 Then mIndP = i
            End If
        End If
    Next i
    Lg "P1", "Multiples found twice (baseline and policy block)", IIf(nS = 2 And nI = 2, "PASS", "FAIL"), _
        LBL_SERV & " x" & nS & " (rows " & mSvcB & ", " & mSvcP & "); " & LBL_IND & " x" & nI & _
        " (rows " & mIndB & ", " & mIndP & ")"
    If nS <> 2 Or nI <> 2 Then Exit Function

    v = Application.Match(YEAR_FIX, mWs.Rows(YEAR_ROW), 0)
    If IsError(v) Then
        Lg "P2", "Column of " & YEAR_FIX & " in row " & YEAR_ROW, "FAIL", "not found"
        Exit Function
    End If
    mCFix = v
    Lg "P2", "Column of " & YEAR_FIX & " in row " & YEAR_ROW, "PASS", "column " & ColName(mCFix)

    mRowB = FindSrvRow(mSvcB)
    mRowP = FindSrvRow(mSvcP)
    Lg "P3", "Services demand row found below each multiple (code " & CODE_SRV & ")", _
        IIf(mRowB > 0 And mRowP > 0, "PASS", "FAIL"), "baseline row " & mRowB & ", policy row " & mRowP
    If mRowB = 0 Or mRowP = 0 Then Exit Function
    mCLast = mWs.Cells(mRowB, mWs.Columns.Count).End(xlToLeft).Column
    mTotB = FindLabelRow(mRowB, LBL_TOT)
    mTotP = FindLabelRow(mRowP, LBL_TOT)

    On Error Resume Next
    nmB = ActiveWorkbook.Names("BaselineFirstRow").RefersToRange.Row
    nmP = ActiveWorkbook.Names("PolicyScenarioFirstRow").RefersToRange.Row
    okNames = (Err.Number = 0)
    Err.Clear
    On Error GoTo 0
    If okNames Then
        Lg "P4", "Block offset equals PolicyScenarioFirstRow - BaselineFirstRow", _
            IIf(mRowP - mRowB = nmP - nmB And mSvcP - mSvcB = nmP - nmB, "PASS", "FAIL"), _
            "found " & (mRowP - mRowB) & ", names " & (nmP - nmB)
    Else
        Lg "P4", "Block offset check", "REVIEW", "names BaselineFirstRow / PolicyScenarioFirstRow not found"
    End If
    Locate = True
End Function

Private Function FindSrvRow(ByVal rMult As Long) As Long
    Dim r As Long
    For r = rMult + 1 To rMult + SCAN_ROWS
        If LCase$(Trim$(mWs.Cells(r, COL_CODE).Text)) = CODE_SRV Then
            If Left$(mWs.Cells(r, mCFix - 1).FormulaR1C1, 10) = "=RC[-1]*R[" Then
                FindSrvRow = r
                Exit Function
            End If
        End If
    Next r
End Function

Private Function FindLabelRow(ByVal r0 As Long, ByVal lbl As String) As Long
    Dim r As Long
    For r = r0 + 1 To r0 + SCAN_ROWS
        If LCase$(Trim$(mWs.Cells(r, COL_LABEL).Text)) = LCase$(lbl) Then
            FindLabelRow = r
            Exit Function
        End If
    Next r
End Function

Private Function RowState(ByVal r As Long, ByVal rInd As Long, ByVal rSvc As Long) As String
    Dim wantBug As String, wantFix As String, j As Long, nB As Long, nF As Long, nCol As Long
    wantBug = "=RC[-1]*R[" & (rInd - r) & "]C"
    wantFix = "=RC[-1]*R[" & (rSvc - r) & "]C"
    nCol = mCLast - mCFix + 1
    For j = mCFix To mCLast
        If mWs.Cells(r, j).FormulaR1C1 = wantBug Then nB = nB + 1
        If mWs.Cells(r, j).FormulaR1C1 = wantFix Then nF = nF + 1
    Next j
    If mWs.Cells(r, mCFix - 1).FormulaR1C1 <> wantFix Then
        RowState = "OTHER"
    ElseIf nB = nCol Then
        RowState = "BUG"
    ElseIf nF = nCol Then
        RowState = "FIXED"
    Else
        RowState = "OTHER"
    End If
End Function

'---------------------------------------------------------------- stage F: the fix

Private Sub ApplyFix()
    Dim rng As Range
    mUndoF(1) = mWs.Range(mWs.Cells(mRowB, mCFix), mWs.Cells(mRowB, mCLast)).FormulaR1C1
    mUndoF(2) = mWs.Range(mWs.Cells(mRowP, mCFix), mWs.Cells(mRowP, mCLast)).FormulaR1C1
    ' baseline: one formula in the first wrong year, dragged right (FillRight = the drag)
    mWs.Cells(mRowB, mCFix).FormulaR1C1 = "=RC[-1]*R[" & (mSvcB - mRowB) & "]C"
    Set rng = mWs.Range(mWs.Cells(mRowB, mCFix), mWs.Cells(mRowB, mCLast))
    rng.FillRight
    ' policy: paste of the baseline row (relative references, so it must work unchanged)
    rng.Copy
    mWs.Cells(mRowP, mCFix).PasteSpecial xlPasteFormulas
    Application.CutCopyMode = False
End Sub

'---------------------------------------------------------------- stage T: tests

Private Sub TestDrag()
    Dim r As Variant, j As Long, ref As String, nBad As Long, w As String
    For Each r In Array(mRowB, mRowP)
        ref = mWs.Cells(r, mCFix - 1).FormulaR1C1
        nBad = 0
        For j = mCFix To mCLast
            If mWs.Cells(r, j).FormulaR1C1 <> ref Then nBad = nBad + 1
        Next j
        Lg "T1", "Drag test, row " & r & ": R1C1 formula identical in " & ColName(mCFix - 1) & ":" & ColName(mCLast), _
            IIf(nBad = 0, "PASS", "FAIL"), ref & "; cells that differ: " & nBad
    Next r
End Sub

Private Sub TestCopyPaste()
    Dim j As Long, nBad As Long
    For j = COL_Y0 To mCLast
        If mWs.Cells(mRowB, j).FormulaR1C1 <> mWs.Cells(mRowP, j).FormulaR1C1 Then nBad = nBad + 1
    Next j
    Lg "T2", "Copy-paste test: policy row R1C1 = baseline row R1C1 in " & ColName(COL_Y0) & ":" & ColName(mCLast), _
        IIf(nBad = 0, "PASS", "FAIL"), "cells that differ: " & nBad & ". The same text pasted from baseline to policy block."
End Sub

Private Sub TestFormulaDiff(fB As Variant, fA As Variant)
    Dim i As Long, j As Long, nExp As Long, nOther As Long, s As String, want As Long
    For i = 1 To mNR
        For j = 1 To mNC
            If fB(i, j) <> fA(i, j) Then
                If (i = mRowB Or i = mRowP) And j >= mCFix And j <= mCLast Then
                    nExp = nExp + 1
                Else
                    nOther = nOther + 1
                    If nOther <= 10 Then s = s & ColName(j) & i & " "
                End If
            End If
        Next j
    Next i
    want = 2 * (mCLast - mCFix + 1)
    Lg "T3", "Only the intended formulas changed (whole sheet, before vs after)", _
        IIf(nOther = 0 And nExp = want, "PASS", "FAIL"), _
        "intended cells changed: " & nExp & " of " & want & "; other cells changed: " & nOther & IIf(nOther > 0, " (first: " & s & ")", "")
End Sub

Private Sub TestIndependent(vA As Variant)
    Dim r As Variant, sv As Long, j As Long, k As Long, jj As Long, nBad As Long, e As Double, a As Variant
    For k = 1 To 2
        If k = 1 Then r = mRowB: sv = mSvcB Else r = mRowP: sv = mSvcP
        nBad = 0
        For j = mCFix To mCLast
            jj = j - COL_Y0 + 1
            e = vA(r, jj - 1) * vA(sv, jj)
            If Abs(vA(r, jj) - e) > TOL * (1 + Abs(e)) Then nBad = nBad + 1
        Next j
        Lg "T4", "Independent recomputation, row " & r & ": value = previous year x services multiple (values after recalculation)", _
            IIf(nBad = 0, "PASS", "FAIL"), "years that differ: " & nBad
    Next k
End Sub

Private Sub TestUnchangedPast(vB As Variant, vA As Variant)
    ' Column K holds totals and maxima over the years in summary rows, and some tables (fiscal
    ' multipliers) use the columns as lags, not years: both can move legitimately. L:M are tested.
    Dim i As Long, j As Long, n As Long, nK As Long, s As String
    For i = 1 To mNR
        If Not SameVal(vB(i, 1), vA(i, 1)) Then nK = nK + 1
        For j = 2 To mCFix - COL_Y0
            If Not SameVal(vB(i, j), vA(i, j)) Then
                n = n + 1
                If n <= 10 Then s = s & ColName(j + COL_Y0 - 1) & i & " "
            End If
        Next j
    Next i
    Lg "T5a", "Column " & ColName(COL_Y0) & " (totals and maxima over the years in summary rows)", "INFO", "cells changed: " & nK
    Lg "T5b", "Years before " & YEAR_FIX & " (columns " & ColName(COL_Y0 + 1) & ":" & ColName(mCFix - 1) & ") unchanged everywhere", _
        IIf(n = 0, "PASS", "REVIEW"), "cells changed: " & n & IIf(n > 0, " (first: " & s & "). A past value that moves is a look-ahead " & _
        "or a table whose columns are lags, not years: open the first cells and decide.", "")
End Sub

Private Sub TestErrors(vB As Variant, vA As Variant)
    Dim i As Long, j As Long, nB As Long, nA As Long
    For i = 1 To mNR
        For j = 1 To mNC - COL_Y0 + 1
            If IsError(vB(i, j)) Then nB = nB + 1
            If IsError(vA(i, j)) Then nA = nA + 1
        Next j
    Next i
    Lg "T6", "Error cells (K:" & ColName(mNC) & ") do not increase", IIf(nA <= nB, "PASS", "FAIL"), "before " & nB & ", after " & nA
End Sub

Private Sub TestTotals(vB As Variant, vA As Variant)
    ' Total demand = sum of the sector rows. Its change equals the services change only if no other
    ' sector moves (a price feedback moves them); the largest share of the other sectors is reported.
    Dim k As Long, r As Long, t As Long, j As Long, jj As Long, dS As Double, dT As Double, w As Double, nOver As Long
    For k = 1 To 2
        If k = 1 Then r = mRowB: t = mTotB Else r = mRowP: t = mTotP
        If t = 0 Then
            Lg "T7", "Total demand row not found below row " & r, "REVIEW", "reconciliation skipped"
        Else
            w = 0: nOver = 0
            For j = mCFix To mCLast
                jj = j - COL_Y0 + 1
                dS = vA(r, jj) - vB(r, jj)
                dT = vA(t, jj) - vB(t, jj)
                If dS <> 0 Then
                    If Abs((dT - dS) / dS) > w Then w = Abs((dT - dS) / dS)
                    If Abs((dT - dS) / dS) > 0.05 Then nOver = nOver + 1
                End If
            Next j
            Lg "T7", "Total demand (row " & t & "): its change minus the services change (row " & r & "), as a share of the services change", _
                IIf(nOver = 0, "PASS", "REVIEW"), "largest share over the years: " & Format(w, "0.0%") & "; years above 5%: " & nOver & _
                ". Other sectors moving = price feedback; check that it is plausible."
        End If
    Next k
End Sub

Private Sub ReportChanges(vB As Variant, vA As Variant)
    ' Rank rows by the largest change as a share of the row's own size (0 to 1), so that rows that
    ' were about zero before do not dominate.
    Dim i As Long, j As Long, n As Long, k As Long, best As Long, sc As Double, mx As Double, d As Double
    Dim rws() As Long, chg() As Double, used() As Boolean, nm As String

    ReDim rws(1 To mNR): ReDim chg(1 To mNR): ReDim used(1 To mNR)
    For i = 1 To mNR
        mx = 0: sc = 0: d = 0
        For j = 1 To mNC - COL_Y0 + 1
            If VarType(vB(i, j)) = vbDouble And VarType(vA(i, j)) = vbDouble Then
                If Abs(vB(i, j)) > sc Then sc = Abs(vB(i, j))
                If Abs(vA(i, j)) > sc Then sc = Abs(vA(i, j))
            End If
        Next j
        For j = 1 To mNC - COL_Y0 + 1
            If Not SameVal(vB(i, j), vA(i, j)) Then
                If VarType(vB(i, j)) = vbDouble And VarType(vA(i, j)) = vbDouble Then
                    If sc > 0 Then d = Abs(vA(i, j) - vB(i, j)) / sc
                    If d > mx Then mx = d
                Else
                    If mx = 0 Then mx = 1
                End If
            End If
        Next j
        If mx > 0 Then
            n = n + 1
            rws(n) = i: chg(n) = mx
        End If
    Next i
    Lg "R1", "Rows with any changed value", "INFO", n & " rows (rows downstream of services electricity: power block, energy and CO2 totals, revenues, ...)"
    For k = 1 To TOP_N
        best = 0
        For i = 1 To n
            If Not used(i) Then
                If best = 0 Then
                    best = i
                ElseIf chg(i) > chg(best) Then
                    best = i
                End If
            End If
        Next i
        If best = 0 Then Exit For
        used(best) = True
        nm = Trim$(mWs.Cells(rws(best), COL_LABEL).Text)
        If nm = "" Then nm = Trim$(mWs.Cells(rws(best), COL_CODE).Text)
        Lg "R2", "Largest change no. " & k & ": row " & rws(best), "INFO", _
            nm & " (code " & mWs.Cells(rws(best), 8).Text & "): largest change = " & Format(chg(best), "0.0%") & " of the row's size"
    Next k
End Sub

'---------------------------------------------------------------- helpers

Private Sub Snap(ByRef f As Variant, ByRef v As Variant)
    f = mWs.Range(mWs.Cells(1, 1), mWs.Cells(mNR, mNC)).FormulaR1C1
    v = mWs.Range(mWs.Cells(1, COL_Y0), mWs.Cells(mNR, mNC)).Value2
End Sub

Private Function SameVal(ByVal a As Variant, ByVal b As Variant) As Boolean
    If IsError(a) Or IsError(b) Then
        If IsError(a) And IsError(b) Then SameVal = (CStr(a) = CStr(b))
        Exit Function
    End If
    If VarType(a) = vbDouble And VarType(b) = vbDouble Then
        SameVal = (Abs(a - b) <= TOL * (1 + Abs(a)))
    Else
        SameVal = (CStr(a) = CStr(b))
    End If
End Function

Private Function ColName(ByVal c As Long) As String
    ColName = Split(mWs.Cells(1, c).Address(True, False), "$")(0)
End Function

Private Sub StartLog()
    Dim ws As Worksheet
    mNFail = 0: mNReview = 0
    Application.DisplayAlerts = False
    On Error Resume Next
    ActiveWorkbook.Worksheets(SH_LOG).Delete
    On Error GoTo 0
    Application.DisplayAlerts = True
    Set mLog = ActiveWorkbook.Worksheets.Add(After:=ActiveWorkbook.Worksheets(ActiveWorkbook.Worksheets.Count))
    mLog.Name = SH_LOG
    mLog.Columns("A:D").NumberFormat = "@"
    mLog.Cells(1, 1).Value = "Fix L1 report (services electricity demand uses the services multiple in every year)"
    mLog.Cells(1, 1).Font.Bold = True
    mLog.Cells(2, 1).Value = "Overall"
    mLog.Cells(2, 2).Value = Format(Now, "yyyy-mm-dd hh:nn")
    mLog.Cells(4, 1).Value = "Step": mLog.Cells(4, 2).Value = "Test": mLog.Cells(4, 3).Value = "Result": mLog.Cells(4, 4).Value = "Detail"
    mLog.Range("A4:D4").Font.Bold = True
    mLogRow = 5
End Sub

Private Sub Lg(ByVal id As String, ByVal what As String, ByVal res As String, ByVal detail As String)
    If res = "FAIL" Then mNFail = mNFail + 1
    If res = "REVIEW" Then mNReview = mNReview + 1
    mLog.Cells(mLogRow, 1).Value = id
    mLog.Cells(mLogRow, 2).Value = what
    mLog.Cells(mLogRow, 3).Value = res
    mLog.Cells(mLogRow, 4).Value = detail
    mLogRow = mLogRow + 1
End Sub
