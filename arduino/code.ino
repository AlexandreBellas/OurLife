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
int led_hbeat = 7;

// Rand
int seed_rand = 0;
int min_rand = 0;
int max_rand = 9;

// Global - Save
float global_hbeat = -1;
float global_pression_systolic = -1;
float global_pression_diastolic = -1;
float global_temperature = -1;
bool push_hbeat = false;
bool push_pression = false;
bool push_temperature = false;
bool push_save = false;

void setup() {
  // Setup ports
  pinMode(input_hbeat, INPUT);
  pinMode(input_pression, INPUT);
  pinMode(input_temperature, INPUT);
  pinMode(button_hbeat, INPUT);
  pinMode(button_pression, INPUT);
  pinMode(button_temperature, INPUT);
  pinMode(button_save, INPUT);
  pinMode(led_hbeat, OUTPUT);
  // Utils
  Serial.begin(9600);
  randomSeed(analogRead(seed_rand));
}

/* -------------------------------- */
/* Heart Beat */
void beat(int led, int t){
  digitalWrite(led, HIGH);
  delay(t);
  digitalWrite(led, LOW);
  delay(t);
}

void heart_beat(){
  // Read
  int read_hbeat = analogRead(input_hbeat);
  int hbeat_adjusted = map(read_hbeat, 0, 1023, 30, 130) - random(min_rand, max_rand);
  global_hbeat = hbeat_adjusted;
  // Print
  Serial.print("Heart Beat: ");
  Serial.print(hbeat_adjusted);
  Serial.println(" bpm");
  // Beat Lead
  int time_hbeat = map(read_hbeat, 0, 1023, 1000, 50);
  beat(led_hbeat, time_hbeat);
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
  global_pression_diastolic = (pression_adjusted - 33 - random(min_rand, max_rand));
  Serial.print("Blood Pressure: ");
  Serial.print(pression_adjusted);
  Serial.print(", ");
  Serial.print(global_pression_diastolic);
  Serial.println(" mmHg");  
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
  Serial.print("Temperature: ");
  Serial.print(temp);
  Serial.println(" C");
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

  Serial.println("Save");
  Serial.println(msg_hbeat);
  Serial.println(msg_pression_systolic);
  Serial.println(msg_pression_diastolic);
  Serial.println(msg_temperature);
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
