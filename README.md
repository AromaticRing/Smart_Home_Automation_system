# 🏠 Smart Home Automation System

A Python-based smart automation system that uses ultrasonic sensors to detect the number of people entering or exiting a room and controls the lighting automatically using a relay.

## 📽️ Demo Video

👉 *[[Demo video link here](https://youtu.be/bF2i0LKluh4)]*

---

## 📌 Project Overview

This system provides a **contactless** and **intelligent** method to automate home lighting using **ultrasonic sensors** and a **relay module**. It counts the number of people in a room by detecting their direction of movement (entry or exit) and turns the light **on/off accordingly**.

If at least one person is present, the light remains **ON**. Once everyone leaves, the light is **automatically turned OFF**.

---

## ⚙️ Features

- 🚶‍♂️ Entry/Exit detection with directional logic (A → B = Entry, B → A = Exit)
- 💡 Automatic relay switching based on presence
- 🧠 Smart reset to avoid stale triggers
- 🔁 Continuous real-time monitoring
- 🛑 Graceful termination with cleanup

---

## 🧰 Technologies & Libraries

- **Python 3**
- **lgpio** (for GPIO handling on Raspberry Pi or compatible boards)
- **Ultrasonic sensors** for proximity/distance measurement
- **Relay module** to control the appliance (e.g., light)

---

## 🛠️ Hardware Components

| Component                    | Quantity |
|-----------------------------|----------|
| Raspberry Pi                | 1        |
| HC-SR04 Ultrasonic Sensor   | 2        |
| 5V Relay Module             | 1        |
| Resistors, Wires            | As needed |
| Breadboard                  | 1        |

---

## 🧪 Working Principle

1. Two ultrasonic sensors (`Sensor A` and `Sensor B`) detect motion near the door.
2. When Sensor A is triggered **before** Sensor B within a short time, it detects an **entry**.
3. When Sensor B is triggered **before** Sensor A, it detects an **exit**.
4. The `person_count` is updated accordingly.
5. The **relay turns ON** if at least one person is present; **turns OFF** otherwise.

---

## 👨‍💻 Authors

Developed by:

- **Anshul Dewangan**
- **Pratyaksh Lodhi**
- **Aaron David Don**
- **Joshua Benchamin**

---

## 📝 License

This project is open-source and available under the [MIT License](LICENSE).

---

## ⚠️ Usage Notes

- Ensure the `lgpio` library is installed using:  
  ```bash
  pip install lgpio


