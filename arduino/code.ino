// Inputs
// batimentos, pressão, temperatura
int input_hbeat = A0;
int input_pression = A1;
int input_temperature = A2;
int button_hbeat = 2;
int button_pression = 3;
int button_temperature = 4;
int button_save = 5;

// Outputs
int led_red = 9;
int led_green = 10;
int led_blue = 11;

// Rand
int seed_rand = 0;
int min_rand = 0;
int max_rand = 8;

// Brightness
int min_brightness = 10;
int max_brightness = 200;

// Global - Save
int global_hbeat = -1;
int global_pression_systolic = -1;
int global_pression_diastolic = -1;
float global_temperature = -1;
bool push_hbeat = false;
bool push_pression = false;
bool push_temperature = false;
bool push_save = false;

/* -------------------------------- */
/* Led RGB */
int brightness(int min_value, int max_value, int value){
  return map(value, min_value, max_value, min_brightness, max_brightness);
}

void led_reset(){
  analogWrite(led_red, min_brightness);
  analogWrite(led_green, min_brightness);
  analogWrite(led_blue, min_brightness);
}

void led_rgb(int red, int green, int blue){
  digitalWrite(led_red, red);
  digitalWrite(led_green, green);
  digitalWrite(led_blue, blue);
}

/* -------------------------------- */
/* Setup */
void setup() {
  // Setup ports
  pinMode(input_hbeat, INPUT);
  pinMode(input_pression, INPUT);
  pinMode(input_temperature, INPUT);
  pinMode(button_hbeat, INPUT);
  pinMode(button_pression, INPUT);
  pinMode(button_temperature, INPUT);
  pinMode(button_save, INPUT);
  
  pinMode(led_red, OUTPUT);
  pinMode(led_green, OUTPUT);
  pinMode(led_blue, OUTPUT);
  // Utils
  Serial.begin(9600);
  randomSeed(analogRead(seed_rand));
  //led_rgb(, min_brightness, min_brightness);
  led_reset();
}

/* -------------------------------- */
/* Heart Beat */
void heart_beat(){
  // Read
  int read_hbeat = analogRead(input_hbeat);
  int hbeat_adjusted = map(read_hbeat, 0, 1023, 30, 130) - random(min_rand, max_rand);
  global_hbeat = hbeat_adjusted;
  // Print
  Serial.print("heart-beat: ");
  Serial.print(hbeat_adjusted);
  Serial.println(" bpm");
  // Beat Lead
  int time_hbeat = map(read_hbeat, 0, 1023, 800, 20);
  //beat(led_hbeat, time_hbeat);
  led_rgb(HIGH, 0, 0);
}

/* -------------------------------- */
/* Pression */
void pression(){
  // Read
  // http://www.assistenciafarmaceutica.far.br/novos-valores-de-referencia-para-hipertensao-o-que-mudou/
  // systolic, diastolic
  int read_pression = analogRead(input_pression);
  int pression_adjusted = map(read_pression, 0, 1023, 60, 150) - random(min_rand, max_rand);
  global_pression_systolic = pression_adjusted;
  global_pression_diastolic = (pression_adjusted - 34 - random(min_rand, max_rand));
  Serial.print("blood-pressure: ");
  Serial.print(pression_adjusted);
  Serial.print(", ");
  Serial.print(global_pression_diastolic);
  Serial.println(" mmHg");
  led_rgb(0, HIGH, 0);
}

/* -------------------------------- */
/* Temperature */
void temperature(){
  // Read
  int read_temperature = analogRead(input_temperature);
  float volt = (read_temperature)*5.0/1024.0;
  float temp = ((volt - 0.5) * 100);
  global_temperature = temp;
  // Print
  Serial.print("temperature: ");
  Serial.print(temp);
  Serial.println(" C");
  int b = brightness(15, 45, temp);
  led_rgb(0, 0, HIGH);
}

/* -------------------------------- */
/* Save */
void save(){
  push_hbeat = push_pression = push_temperature = false;
  String msg_hbeat = (global_hbeat == -1) ? "-" : String(global_hbeat);
  String msg_pression_systolic = (global_pression_systolic == -1) ? "-" : String(global_pression_systolic);
  String msg_pression_diastolic = (global_pression_diastolic == -1) ? "-" : String(global_pression_diastolic);
  String msg_temperature = (global_temperature == -1) ? "-" : String(global_temperature);
  global_hbeat = global_pression_systolic = global_pression_diastolic = global_temperature = -1;

  Serial.println("save");
  Serial.println(msg_hbeat);
  Serial.println(msg_pression_systolic);
  Serial.println(msg_pression_diastolic);
  Serial.println(msg_temperature);
  led_reset();
}
/* -------------------------------- */
/* Loop */
void loop() {
  /* -------------------------------- */
  // Read - Button
  int read_button_hbeat = digitalRead(button_hbeat);
  int read_button_pression = digitalRead(button_pression);
  int read_button_temperature = digitalRead(button_temperature);
  int read_button_save = digitalRead(button_save);
  // Process
  push_save = (read_button_save == 1) ? true : false;
  push_hbeat = (read_button_hbeat == 1 || (push_hbeat && push_pression == push_temperature)) ? true : false;
  push_pression = (read_button_pression == 1 || (push_pression && read_button_hbeat == push_temperature)) ? true : false;
  push_temperature = (read_button_temperature == 1 || (push_temperature && read_button_hbeat == read_button_pression)) ? true : false;

  /* -------------------------------- */
  // Sensors
  if(push_save) save(); // Save Global Data
  else if(push_hbeat) heart_beat(); // Heart Beat
  else if(push_pression) pression(); // Pression
  else if(push_temperature) temperature(); // Temperature

  delay(200);
}
