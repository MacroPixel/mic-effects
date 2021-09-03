toggle := true
return

NumpadDiv::
toggle := !toggle
return

NumpadIns::
if toggle {
file := FileOpen( "data.txt", "w" )
file.write( "0" )
file.close()
}
else send {Insert}
return

NumpadAdd::
if toggle {
file := FileOpen( "data.txt", "w" )
file.write( "1" )
file.close()
}
else send {+}
return

NumpadEnd::
if toggle {
file := FileOpen( "data.txt", "w" )
file.write( "2" )
file.close()
}
else send {End}
return

NumpadSub::
if toggle {
file := FileOpen( "data.txt", "w" )
file.write( "-" )
file.close()
}
else send {-}
return

NumpadEnter::
if toggle {
file := FileOpen( "data.txt", "w" )
file.write( "ENTER" )
file.close()
}
else send {Enter}
return