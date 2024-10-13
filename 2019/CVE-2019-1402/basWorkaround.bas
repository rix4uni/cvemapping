Option Compare Database
Option Explicit

Private Const WorkaroundTableSuffix As String = "_Table"

Public Sub AddWorkaroundForCorruptedQueryIssue()
    On Error Resume Next
    
    With CurrentDb
        Dim tableDef As tableDef
        For Each tableDef In .tableDefs
            Dim isSystemTable As Boolean
            isSystemTable = tableDef.Attributes And dbSystemObject
            
            If Not EndsWith(tableDef.Name, WorkaroundTableSuffix) And Not isSystemTable Then
                Dim originalTableName As String
                originalTableName = tableDef.Name
                
                tableDef.Name = tableDef.Name & WorkaroundTableSuffix
                
                Call .CreateQueryDef(originalTableName, "select * from [" & tableDef.Name & "]")
                
                Debug.Print "OldTableName/NewQueryName" & vbTab & "[" & originalTableName & "]" & vbTab & _
                            "NewTableName" & vbTab & "[" & tableDef.Name & "]"
            End If
        Next
    End With
End Sub

Public Sub RemoveWorkaroundForCorruptedQueryIssue()
    On Error Resume Next
    
    With CurrentDb
        Dim tableDef As tableDef
        For Each tableDef In .tableDefs
            Dim isSystemTable As Boolean
            isSystemTable = tableDef.Attributes And dbSystemObject
            
            If EndsWith(tableDef.Name, WorkaroundTableSuffix) And Not isSystemTable Then
                Dim originalTableName As String
                originalTableName = Left(tableDef.Name, Len(tableDef.Name) - Len(WorkaroundTableSuffix))
                
                Dim workaroundTableName As String
                workaroundTableName = tableDef.Name
                
                Call .QueryDefs.Delete(originalTableName)
                tableDef.Name = originalTableName
                
                Debug.Print "OldTableName" & vbTab & "[" & workaroundTableName & "]" & vbTab & _
                            "NewTableName" & vbTab & "[" & tableDef.Name & "]" & vbTab & "(Query deleted)"
            End If
        Next
    End With
End Sub

'From https://excelrevisited.blogspot.com/2012/06/endswith.html
Private Function EndsWith(str As String, ending As String) As Boolean
     Dim endingLen As Integer
     endingLen = Len(ending)
     EndsWith = (Right(Trim(UCase(str)), endingLen) = UCase(ending))
End Function
