#include <M5Cardputer.h>
#include <M5Unified.h>
#include <M5GFX.h>
#include <SD.h>
#include <SPI.h>

M5GFX display;
M5Canvas canvas(&display);


#define SD_SPI_SCK  40
#define SD_SPI_MISO 39
#define SD_SPI_MOSI 14
#define SD_SPI_CS   12

const char* BANNED_TOKENS[] = {"os", "subprocess", "eval", "exec", "open", "system", "shutil", "getattr"};
const int TOKEN_COUNT = 8;

const char* ROASTS[] = {
    "Nice try, Dr. Hackerman. Submission denied.",
    "My grandmother writes cleaner code, and she's a ceramic cat.",
    "Syntax violation detected. Go sit in the corner.",
    "Security breach blocked. I have logged your mother's IP."
};
const int ROAST_COUNT = 4;


String fileList[40]; 
int fileCount = 0;
int currentSelection = 0;
int scrollOffset = 0;        
const int MAX_VISIBLE_ROWS = 4; 
bool insideScanScreen = false;


void playSuccessChirp() {
    M5Cardputer.Speaker.setVolume(64); 
    M5Cardputer.Speaker.tone(880, 100);  
    delay(100);
    M5Cardputer.Speaker.tone(1318, 150); 
    delay(150);
    M5Cardputer.Speaker.stop();
}

void playAlarmNoise() {
    M5Cardputer.Speaker.setVolume(128); 
    for (int i = 0; i < 3; i++) {
        M5Cardputer.Speaker.tone(600, 150);
        delay(150);
        M5Cardputer.Speaker.tone(300, 150);
        delay(150);
    }
    M5Cardputer.Speaker.stop();
}

void drawMenu() {
    canvas.fillScreen(BLACK);
    canvas.setCursor(0, 0);
    
    canvas.setTextColor(CYAN, BLACK);
    canvas.println("= S.A.S.S.I. EXPLORER [W/S/Ent] =");
    canvas.println("---------------------------------");

    if (fileCount == 0) {
        canvas.setTextColor(WHITE, BLACK);
        canvas.println(" No Python (.py) files found.");
    } else {
        int endRow = scrollOffset + MAX_VISIBLE_ROWS;
        if (endRow > fileCount) endRow = fileCount;

        for (int i = scrollOffset; i < endRow; i++) {
            if (i == currentSelection) {
                canvas.setTextColor(BLACK, GREEN); 
                canvas.print("> ");
                canvas.println(fileList[i]);
            } else {
                canvas.setTextColor(WHITE, BLACK);
                canvas.print("  ");
                canvas.println(fileList[i]);
            }
        }
        
        if (fileCount > MAX_VISIBLE_ROWS) {
            canvas.setTextColor(0x7BEF, BLACK);
            canvas.printf("\n--- Item %d/%d ---", currentSelection + 1, fileCount);
        }
    }
    canvas.pushSprite(0, 0);
}

void printToScreen(const char* text, uint16_t color = WHITE) {
    canvas.setTextColor(color);
    canvas.println(text);
    canvas.pushSprite(0, 0);
}

void executeScan(String fileName) {
    insideScanScreen = true;
    canvas.fillScreen(BLACK);
    canvas.setCursor(0, 0);
    
    String header = "TARGET PROTOCOL: " + fileName;
    printToScreen(header.c_str(), CYAN);
    printToScreen("Reading data streams...", WHITE);

    File f = SD.open("/" + fileName);
    if (!f) {
        printToScreen("❌ Error: Could not open file!", RED);
        delay(3000);
        insideScanScreen = false;
        return;
    }

    bool violation_found = false;
    String bad_token = "";

    while (f.available()) {
        String line = f.readStringUntil('\n');
        line.trim();

        for (int i = 0; i < TOKEN_COUNT; i++) {
            if (line.indexOf(BANNED_TOKENS[i]) >= 0) {
                violation_found = true;
                bad_token = String(BANNED_TOKENS[i]);
                break;
            }
        }
        if (violation_found) break;
    }
    f.close();

    if (violation_found) {
        playAlarmNoise();
        String msg = "⚠ BANNED TOKEN: " + bad_token;
        printToScreen(msg.c_str(), RED);
        int roastIdx = random(ROAST_COUNT);
        printToScreen(ROASTS[roastIdx], YELLOW);
    } else {
        playSuccessChirp();
        printToScreen("✓ No violations detected.", GREEN);
    }

    printToScreen("Press any key to return...", WHITE);
    delay(500);
    
   
    M5Cardputer.Keyboard.isChange(); 
    while (true) {
        M5Cardputer.update();
        if (M5Cardputer.Keyboard.isChange() && M5Cardputer.Keyboard.isPressed()) {
            break;
        }
        delay(30);
    }
    insideScanScreen = false;
    drawMenu();
}


void populateFileList() {
    File root = SD.open("/");
    fileCount = 0;
    while (true) {
        File entry = root.openNextFile();
        if (!entry) break; 
        
        String name = String(entry.name());
        if (!entry.isDirectory() && name.endsWith(".py") && fileCount < 40) {
            fileList[fileCount] = name;
            fileCount++;
        }
        entry.close();
    }
    root.close();
}


void setup() {
    auto cfg = M5.config();
    M5Cardputer.begin(cfg, true);
    
    display.begin();
    display.setRotation(1); 
    canvas.setColorDepth(8);
    canvas.createSprite(display.width(), display.height());
    canvas.setTextSize(1); 
    
    canvas.fillScreen(BLACK);
    printToScreen("S.A.S.S.I. Booting Local Mode...", CYAN);
    
    M5Cardputer.Speaker.begin();
    
    SPI.begin(SD_SPI_SCK, SD_SPI_MISO, SD_SPI_MOSI, SD_SPI_CS);
    if (!SD.begin(SD_SPI_CS, SPI, 25000000)) {
        printToScreen("❌ SD Card Mount Failed!", RED);
        while (true) { delay(1000); }
    }
    
    populateFileList();
    drawMenu();
}

void loop() {
    M5Cardputer.update();
    
    if (!insideScanScreen) {
        if (M5Cardputer.Keyboard.isKeyPressed('w')) {
            if (currentSelection > 0) {
                currentSelection--;
                if (currentSelection < scrollOffset) scrollOffset = currentSelection;
            }
            drawMenu();
        } 
        else if (M5Cardputer.Keyboard.isKeyPressed('s')) {
            if (currentSelection < fileCount - 1) {
                currentSelection++;
                if (currentSelection >= scrollOffset + MAX_VISIBLE_ROWS) scrollOffset = currentSelection - MAX_VISIBLE_ROWS + 1;
            }
            drawMenu();
        }
        
        Keyboard_Class::KeysState status = M5Cardputer.Keyboard.keysState();
        if (status.enter && fileCount > 0) {
            executeScan(fileList[currentSelection]);
        }
    }
    delay(30);
}
