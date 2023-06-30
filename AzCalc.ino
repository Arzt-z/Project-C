//ESP32
  #include <TFT_eSPI.h> // Hardware-specific library
  #include <SPI.h>
  #include "tinyexpr.h"
  #include "UI.h"


  TFT_eSPI tft = TFT_eSPI();  //pantalla
  int displayWidth = 320;
  int displayHeight = 240;
  UI ui(tft, displayWidth , displayHeight);
//vars pins keypad
  int keypadOUT[4] = {13, 12, 14, 27};
  int kpMulxOUT[4] = {26, 25, 33, 32};
  int keymapmode = 1;
  int kpMulxDAT = 34;
//end vars pins keypad
//display vars
  int screenled = 5;
  const int freq = 5000;
  const int ledChannel = 0;
  const int resolution = 8;

//end display vars
//keymap matrix calcmode
  String keyMap1[4][14] = {
  //0       1       2         3       4        5       6        7         8          9       10         11         12        13
  {"0",    ".",  "<EXP>",  "<ANS>",  "=",     ""  ,    ""  ,  "<UP>",  "<DOWN>", "<LOG>" , "^(1/" ,  "<CALC>", "<SHIFT>",   ""     },//0
  {"1",    "2",    "3"  ,    "+"  ,  "-",   "<IN>", "<OUT>",     ",",    "^"   ,   "^2"  ,   "^3" , "<SOLVE>", "<ALPHA>",   ""     },//1
  {"4",    "5",    "6"  ,    "*"  ,  "/",   "(-)" ,   ";"  , "<HYP>",   "sin(" , "COS("  , "TAN(" ,  "<STO>" ,  "<LEFT>",  "<AC>"  },//2
  {"7",    "8",    "9"  , "<DEL>" ,   "",  "<RCL>", "<ENG>",     "(",     ")"  , "<ab/c>", "<M+>" ,   "<LN>" ,  "<RIGH>", "<OMEGA>"} //3
  };
  String keyMap2[4][14] = {
  //0       1       2         3       4        5       6        7         8          9       10         11         12        13
  {"0",    ".",    "x"  ,    "y"  ,  "=",     ""  ,    ""  ,  "<UP>",  "<DOWN>",    "e"  ,   "f"  ,    "a"   , "<SHIFT>",   ""     },//0
  {"1",    "2",    "3"  ,    "+"  ,  "-",   "<IN>", "<OUT>",     ",",    "^"   ,   "^2"  ,   "^3" ,    "b"   , "<ALPHA>",   ""     },//1
  {"4",    "5",    "6"  ,    "*"  ,  "/",   "(-)" ,   ";"  , "<HYP>",   "sin(" , "COS("  , "TAN(" ,    "c"   ,  "<LEFT>",  "<AC>"  },//2
  {"7",    "8",    "9"  , "<DEL>" ,   "",  "<RCL>", "<ENG>",     "(",     ")"  , "<ab/c>", "<M+>" ,    "d"   ,  "<RIGH>", "<OMEGA>"} //3
  };
  String buffer ="";
  String key ="";
//


void setup() {
  Serial.begin(115200);
  ui.begin(); 
  setupPins(); //setup pins y pinled display

}
  

void loop() {
  //ui.drawBorder(5, 5, dpWidth-10, 40, 5, 5,10,15);


  key = getKey();

  if (!key.isEmpty()) {
    buffer = ui.updateBuffer(buffer,key);
    ui.cleanResultBox();
    ui.printResult(String(te_interp(buffer.c_str(), 0)));
    if(buffer =="sin(x)"){
      ui.SIN(1 , 0);
    }
  }

  delay(100);
}

void setupScreen(){

  //tft.setTextColor(TFT_BLACK, TFT_WHITE); //invierte los colores fondo y texto *cambiar fill screen por white tambien.
}

void setupPins(){
  for(int i=0;i<4;i++){
    pinMode(keypadOUT[i], OUTPUT);
    pinMode(kpMulxOUT[i], OUTPUT);
  }
  pinMode(kpMulxDAT, INPUT);
  ledcSetup(ledChannel,freq,resolution);
  ledcAttachPin(screenled, ledChannel);
  ledcWrite(ledChannel,  200);
}

void setMuxChannel(byte channel){
  for(int i=0;i<4;i++){
    digitalWrite(kpMulxOUT[i], bitRead(channel, i));
  }
}

void updateBuffer(String mykey){
  tft.setTextSize(3);
  if(mykey == "<DEL>"){
    buffer = buffer.substring(0, buffer.length() - 1);
    tft.drawString( buffer,10,10);
    tft.setTextSize(2);
    return ;
  }
  if (!key.isEmpty()) {
    buffer = buffer + mykey;
    tft.drawString( buffer,10,10);
  }
  tft.setTextSize(2);
  return ;
}

String getKey(){
  for(int j=0;j<4;j++){
    setALLOFF();
    digitalWrite(keypadOUT[j], HIGH);
    for(int i=0;i<14;i++){
      setMuxChannel(i); 
      if(((int) (analogRead(kpMulxDAT)))>500){
        //tft.fillScreen(TFT_BLACK);
        if(keyMap1[j][i]=="<ALPHA>"){
          keymapmode = keymapmode*(-1);
          return "";
        }
        if(keymapmode == 1){
          return keyMap1[j][i];
        }
        if(keymapmode == (-1)){
          return keyMap2[j][i];
        }
      }
    }
  }
  return "";
}

int setALLON(){
  for(int i=0;i<4;i++){
    digitalWrite(keypadOUT[i], HIGH);
  }
}

int setALLOFF(){
  for(int i=0;i<4;i++){
    digitalWrite(keypadOUT[i], LOW);
  }
}