
void splash2( int row, String txt)
{
  int curs = (21 - txt.length()) / 2;
  lcd.setCursor(0, row);
  lcd.print("--------------------");
  lcd.setCursor(curs, row);
  lcd.print(txt);
  delay(70);
}
