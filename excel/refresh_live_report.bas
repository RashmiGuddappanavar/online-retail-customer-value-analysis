' VBA Module for Refreshing Live MySQL / SQLite Analytical Data in Excel
' Online Retail Customer Value & Revenue Analytics

Sub RefreshLiveReport()
    Dim pt As PivotTable
    Dim ws As Worksheet
    
    On Error GoTo ErrorHandler
    
    ' Refresh all data connections connected to MySQL / Live Database Views
    ActiveWorkbook.RefreshAll
    
    ' Explicitly refresh pivot tables
    For Each ws In ActiveWorkbook.Worksheets
        For Each pt In ws.PivotTables
            pt.Update
        Next pt
    Next ws
    
    MsgBox "Excel Management Dashboard refreshed successfully from Live Analytical Database!", vbInformation, "Live Data Refresh Complete"
    Exit Sub

ErrorHandler:
    MsgBox "Error refreshing live data report: " & Err.Description, vbCritical, "Refresh Error"
End Sub
