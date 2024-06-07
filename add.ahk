#SingleInstance, Force

; Set the path to your text file
TextFilePath := "test.txt"

; Set the image paths according to your current directory
AddButtonImage := "add.png"
InputBoxImage := "input.png"
OkButtonImage := "ok.png"
Sleep 5000 
;ImageSearch, FoundX, FoundY, 0, 0, A_ScreenWidth, A_ScreenHeight, %AddButtonImage%
;    if ErrorLevel = 0
;    {
;        Click, %foundX%, %foundY%
;    }
Loop, read, %TextFilePath% 
{
 Clipboard := A_LoopReadLine
 ImageSearch, FoundX, FoundY, 0, 0, A_ScreenWidth, A_ScreenHeight, %AddButtonImage%
 if ErrorLevel = 0
 {
  Click, %foundX%, %foundY%
  Sleep 200
  ImageSearch, FoundX, FoundY, 0, 0, A_ScreenWidth, A_ScreenHeight, %InputBoxImage%
  if ErrorLevel = 0
  {
   ;Click, %foundX%, %foundY%
   ;Sleep 1000
   Send, ^v
   Sleep 200
   ImageSearch, FoundX, FoundY, 0, 0, A_ScreenWidth, A_ScreenHeight, %OkButtonImage%
   if ErrorLevel = 0
   {
    Click, %foundX%, %foundY%
    Sleep 200
   }
  }
 }
}