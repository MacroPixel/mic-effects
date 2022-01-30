toggle := true
debug := false
return



write_data( value ) {
  global debug
  if debug
    msgbox %value%
  else {
    file := FileOpen( "data.txt", "w" )
    file.write( value )
    file.close()
  }
}



NumpadDel::
toggle := !toggle
return



NumpadDiv::
if toggle
  write_data( "div_normal" )
else send /



NumpadMult::
if !toggle
  send *
return



*NumpadAdd::
if toggle {
  write_data( "add_normal" )
}
else send {+}
return



*NumpadIns::
if toggle {

  if GetKeyState( "NumpadMult", "P" )
    write_data( "0_sb" )
  else
    write_data( "0_normal" )
    
}
else send {Insert}
return



*NumpadEnd::
if toggle {

  if GetKeyState( "NumpadMult", "P" )
    write_data( "1_sb" )
  else
    write_data( "1_normal" )
    
}
else send {End}
return



*NumpadDown::
if toggle {

  if GetKeyState( "NumpadMult", "P" )
    write_data( "2_sb" )
  else
    write_data( "2_normal" )

}
else send {NumpadDown}
return



*NumpadPgDn::
if toggle {

  if GetKeyState( "NumpadMult", "P" )
    write_data( "3_sb" )
    
}
else send {NumpadPgDn}
return



*NumpadPgUp::
if toggle {

  if GetKeyState( "NumpadMult", "P" )
    write_data( "9_sb" )
  else
    write_data( "9_normal" )
    
}
else send {NumpadPgUp}
return



*NumpadSub::
if toggle
  write_data( "sub" )
else send {-}
return



*NumpadEnter::
if toggle {

  if GetKeyState( "NumpadMult", "P" )
    write_data( "enter_sb" )
  else
    write_data( "enter_normal" )
    
}
else send {Enter}
return