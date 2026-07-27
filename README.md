# S.A.S.S.I. — Static Analysis Script Security Inspector 🛡️

S.A.S.S.I. is a fully local, zero-dependency python script safety inspector built explicitly for the **M5Stack Cardputer ADV** as part of the Hack Club Portputer YSWS. 

It lets you pop in a MicroSD card containing Python code files, use your physical keyboard to navigate through them, and instantly run a security scan line-by-line to catch malicious or restricted function usage before deployment. If it passes, it chirps a harmonic melody. If it fails, it sounds a harsh alarm sequence and aggressively roasts the developer.

---

##  Features
* **100% Local Processing:** Runs entirely on-device without needing internet connectivity or a companion system!!!!.
* **Dynamic Screen Navigation:** Scroll-safe file viewer maps your SD root directory instantly, adapting smoothly with viewport tracking loops.
* **Static Token Chasing:** Catches complex or dangerous structural tokens like `os`, `subprocess`, `eval`, `exec`, `open`, `system`, and `shutil`.
* **Hardware Audio Feedback:** Uses the native Cardputer speaker PWM clock to alert you with high-low alarm loops (on failure) or smooth chirps (on passing).

---

##  Hardware Setup & Pinout
Ensure your MicroSD card is formatted to **FAT32** and has a few `.py` files sitting right at the root directory level.

This project relies on the native **Cardputer ADV SPI node layout**:
* **MISO:** Pin 39
* **MOSI:** Pin 14
* **SCK:** Pin 40
* **CS:** Pin 12

---

##  Flashing via Arduino IDE

### 1. Library Dependencies
Before clicking upload, make sure you have installed these exact official libraries via the **Arduino Library Manager**:
1. `M5Cardputer`
2. `M5Unified`
3. `M5GFX`

### 2. Compilation Target
1. Open `CardputerDogApp.ino` in your IDE.
2. Go to **Tools** > **Board** > **ESP32 Arduino** and select **M5Stack-Cardputer**.
3. Plug in your hardware over USB-C, choose your active serial port, and hit **Upload** (Right Arrow icon).

---

##  How to Use It
1. Use **`W`** (Up) and **`S`** (Down) on your physical keyboard to move the selector cursor.
2. Press **`Enter`** to initialize a code target sweep scan.
3. Once the scan is complete, press **any key** on the keyboard matrix layout to exit back to the file manager explorer.
