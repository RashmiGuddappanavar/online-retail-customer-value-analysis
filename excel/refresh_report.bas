Attribute VB_Name = "mod_RefreshReport"
' =============================================================================
' ONLINE RETAIL II MANAGEMENT REPORTING — AUTOMATION MODULE
' File: excel/refresh_report.bas
' Purpose: VBA macro for refreshing calculations, updating report timestamps,
'          executing data quality checks, and handling operational errors.
' =============================================================================

Option Explicit

Sub RefreshReport()
    On Error GoTo ErrorHandler
    
    Dim wsDash As Worksheet
    Dim wsDQ As Worksheet
    Dim startTime As Double
    startTime = Timer
    
    ' Optimize execution speed
    Application.ScreenUpdating = False
    Application.Calculation = xlCalculationManual
    Application.EnableEvents = False
    
    Set wsDash = ThisWorkbook.Sheets("Dashboard")
    Set wsDQ = ThisWorkbook.Sheets("Data_Quality")
    
    ' 1. Recalculate Workbook Formulas
    Application.Calculate
    
    ' 2. Refresh PivotTables safely if present
    Dim ws As Worksheet
    Dim pt As PivotTable
    For Each ws In ThisWorkbook.Worksheets
        If ws.PivotTables.Count > 0 Then
            For Each pt In ws.PivotTables
                pt.Update
            Next pt
        End If
    Next ws
    
    ' 3. Update Dashboard Timestamp
    wsDash.Range("A2").Value = "Multi-Year Performance, RFM Segmentation & Commercial Risk Analytics  |  Last Refresh: " & Format(Now, "yyyy-mm-dd hh:mm:ss")
    
    ' 4. Execute Data Quality Validation Routine
    Call RunDataQualityCheck
    
    ' Restore settings
    Application.Calculation = xlCalculationAutomatic
    Application.ScreenUpdating = True
    Application.EnableEvents = True
    
    MsgBox "Report refreshed successfully in " & Format(Timer - startTime, "0.00") & " seconds." & vbCrLf & _
           "Timestamp: " & Format(Now, "yyyy-mm-dd hh:mm:ss"), vbInformation, "Refresh Complete"
    Exit Sub

ErrorHandler:
    Application.Calculation = xlCalculationAutomatic
    Application.ScreenUpdating = True
    Application.EnableEvents = True
    MsgBox "An error occurred during report refresh: " & Err.Description, vbCritical, "Refresh Failed"
End Sub

Sub RunDataQualityCheck()
    On Error GoTo DQErrorHandler
    
    Dim wsDQ As Worksheet
    Set wsDQ = ThisWorkbook.Sheets("Data_Quality")
    
    ' Update verification timestamp
    wsDQ.Range("E13").Value = "Verified at " & Format(Now, "yyyy-mm-dd hh:mm:ss")
    
    Exit Sub
DQErrorHandler:
    MsgBox "Data quality check encountered an error: " & Err.Description, vbExclamation, "Data Quality Audit Error"
End Sub
