#include <M5Cardputer.h>


const int NUM_TOKENS = 7;
const String BANNED_TOKENS[NUM_TOKENS] = {
  "os", "subprocess", "eval", "exec", "open", "system", "shutil"
};


const int NUM_ROASTS = 3;
const String ROASTS[NUM_ROASTS] = {
  "Nice try, Dr. Hackerman. Submission denied.",
  "Syntax violation detected. Go sit in a corner.",
  "Security breach blocked. MAC address logged."
};

String currentInputText = "";

void displayHeader() {
  M5Cardputer.Display.fillScreen(BLACK);
  M5Cardputer.Display.setCursor(0, 0);
  M5Cardputer.Display.setTextColor(CYAN);
  M5Cardputer.Display.println("=============================");
  M5Cardputer.Display.println("  S.A.S.S.I. ADV PORTABLE   ");
  M5Cardputer.Display.println("=============================");
  M5Cardputer.Display.setTextColor(WHITE);
  M5Cardputer.Display.print("Code: ");
}

void processSubmittedCode(String inputCode) {
  M5Cardputer.Display.fillScreen(BLACK);
  M5Cardputer.Display.setCursor(0, 0);
  M5Cardputer.Display.setTextColor(YELLOW);
  M5Cardputer.Display.println("[!] INITIALIZING SCANNER...");
  delay(600);

  String currentToken = "";
  bool breachDetected = false;
  String triggeredToken = "";


  for (size_t k = 0; k < inputCode.length(); k++) {
    char c = inputCode[k];

    if (isspace(c) || c == '(' || c == ')' || c == '[' || c == ']' || c == ',' || c == '.' || c == ':' || c == ';') {
      if (currentToken.length() > 0) {
        
     
        for (int i = NUM_TOKENS - 1; i >= 0; i--) {
          if (currentToken == BANNED_TOKENS[i]) {
            breachDetected = true;
            triggeredToken = currentToken;
            break;
          }
        }
        currentToken = ""; 
      }
      if (breachDetected) {
        break;
      }
    } 
    else {
      currentToken += c;
    }
  }

  
  if (!breachDetected && currentToken.length() > 0) {
    for (int i = NUM_TOKENS - 1; i >= 0; i--) {
      if (currentToken == BANNED_TOKENS[i]) {
        breachDetected = true;
        triggeredToken = currentToken;
      }
    }
  }

 
  M5Cardputer.Display.fillScreen(BLACK);
  M5Cardputer.Display.setCursor(0, 10);

  if (breachDetected) {
    M5Cardputer.Display.setTextColor(RED);
    M5Cardputer.Display.print("[BLOCK] Detected: ");
    M5Cardputer.Display.println(triggeredToken);
    M5Cardputer.Display.setCursor(0, 45);
    M5Cardputer.Display.setTextColor(ORANGE);
    
    int randomIdx = random(0, NUM_ROASTS);
    M5Cardputer.Display.println(ROASTS[randomIdx]);
  } else {
    M5Cardputer.Display.setTextColor(GREEN);
    M5Cardputer.Display.println("[PASSED] Code logic clear.");
    M5Cardputer.Display.println("Secure and profoundly boring.");
  }

  M5Cardputer.Display.setTextColor(WHITE);
  M5Cardputer.Display.setCursor(0, 110);
  M5Cardputer.Display.println("Press [ENTER] to cycle...");
}

void setup() {
  auto cfg = M5.config();
  M5Cardputer.begin(cfg, true); 
  M5Cardputer.Display.setRotation(1); 
  M5Cardputer.Display.setTextSize(1.5); 
  
  randomSeed(analogRead(0));
  displayHeader();
}

void loop() {
  M5Cardputer.update();

  
  if (M5Cardputer.Keyboard.isPressed()) {
    if (M5Cardputer.Keyboard.isKeyPressed(KEY_ENTER)) {
      if (currentInputText.length() > 0) {
        processSubmittedCode(currentInputText);
        currentInputText = "";
        while (M5Cardputer.Keyboard.isPressed()) { M5Cardputer.update(); } 
        while (!M5Cardputer.Keyboard.isKeyPressed(KEY_ENTER)) { M5Cardputer.update(); } 
      }
      displayHeader();
    }
    else if (M5Cardputer.Keyboard.isKeyPressed(KEY_BACKSPACE)) {
      if (currentInputText.length() > 0) {
        currentInputText.remove(currentInputText.length() - 1);
        displayHeader();
        M5Cardputer.Display.print(currentInputText);
      }
    }
    else {
      
      Keyboard_Class::KeysState status = M5Cardputer.Keyboard.keysState();
      for (auto i : status.word) {
        currentInputText += i;
        M5Cardputer.Display.print(i);
      }
    }
    
  
    delay(150);
  }
}
