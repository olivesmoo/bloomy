# Bloomy: A Robotic Flower for Intuitive Air Quality Monitoring

Olivia Mei (om228@cornell.edu), Helenna Yin (yy2294@cornell.edu), Yuval Steimberg (ys2335@cornell.edu), Nana Takada (nt388@cornell.edu)

INFO 5342: Designing Ubiquitous and Interactive Computing Devices

## Abstract
Asthma is a chronic respiratory condition that af-
fects millions worldwide, with symptoms often triggered by poor
indoor air quality. Despite the health risks posed by pollutants
such as PM2.5 and CO 2 , existing monitoring systems often rely
on passive digital interfaces that require users to interpret graphs
or numerical indicators—barriers that limit real-time awareness
and action. In response, we present Bloomy, a robotic flower
that functions as an intuitive, ambient air quality companion.
Bloomy expresses environmental conditions through tangible
feedback—blooming or closing its petals and changing LED
colors based on sensor data—offering an emotionally resonant
alternative to traditional displays.

Our system combines real-time sensing, wireless communication, and expressive actuation using a custom-designed rack-and-pinion mechanism driven by a stepper motor. We describe our
iterative design and fabrication process, including the integration of NeoPixels, microcontrollers, and 3D-printed components
within a lotus-inspired form factor. We also detail challenges
related to power constraints, mechanical tolerances, and system-level integration, and share lessons learned from prototyping and user feedback.

Bloomy demonstrates the feasibility and appeal of tangible
interfaces for health-related monitoring, especially in the context
of asthma awareness. It transforms invisible environmental risks
into visible, glanceable feedback and serves as a foundation for
future work in ambient, emotionally engaging health technologies.

## I. INTRODUCTION
Asthma is a prevalent health concern, with the Centers for
Disease Control and Prevention estimating that 1 in 13 Ameri-
cans suffer from the condition. Episodes are often triggered by
poor air quality, particularly indoor pollutants such as volatile
organic compounds (VOCs), carbon dioxide (CO 2 ), and fine
particulate matter (PM2.5). While numerous digital tools exist
to monitor air quality, many require active checking of apps
or interpretation of complex visualizations—barriers that often
reduce sustained engagement and real-time action.

Studies have shown that users benefit from glanceable and
tangible representations of data, which lower the cognitive
barrier to awareness and prompt more immediate behavioral
responses [3], [5]. Inspired by this, we designed Bloomy: a
robotic flower that communicates air quality through simple,
universally understood metaphors—color and blooming. The
flower opens and glows green when air is clean, partially
closes and glows yellow when conditions are moderate, and
fully closes with a red alert when poor air quality is detected.
These states map clearly to a user’s mental model of environmental health, requiring no technical background or explicit
data interpretation.

Our goals with Bloomy were threefold: (1) to create a fully
functional and responsive environmental sensing system, (2)
to translate complex air quality data into emotionally engaging
physical output, and (3) to develop a solution that is aesthet-
ically pleasing and suitable for home environments. In what
follows, we describe our end-to-end process—from component
selection and prototyping to BLE-based communication and
feedback logic—alongside challenges, iterations, and final
insights. We hope Bloomy provides both a technical and
experiential contribution to the field of ambient and tangible
computing.

## II. RELATEDWORK

Commercial and academic systems have long explored
how to represent environmental data to end users, but most
rely heavily on numeric or graphical outputs, which can be
cognitively demanding or easily ignored.

Products like the Atmotube PRO [2] provide highly accurate
real-time environmental data but present it in a format that
requires users to engage with a mobile app to make sense
of the information. This introduces friction in everyday use
and limits the ability for users to respond quickly to changing
conditions. Even with push notifications, the abstract nature of
numerical scores or air quality indices requires interpretation
that may not be intuitive to all users, especially children or
the elderly.

The inAir studies by Kim and Paulos [3], [4] aimed to
address this challenge by introducing ambient visualizations of
indoor air quality. Their work demonstrated that even simple
graphs shown in the periphery of a user’s environment could
improve awareness. However, these systems still required users
to observe and decode visual patterns and lacked physical
interactivity or emotional engagement. Our project builds on
this notion by translating air quality into expressive physical
behaviors that can be observed at a glance and felt intuitively.
Further, studies such as those by Wong-Parodi et al. [5] and
Zhou and Sampath [6] show that users respond more positively
and take more proactive health actions when environmental
feedback is tangible, immediate, and embedded within their
living space. Devices that integrate sensing and feedback into
a unified and meaningful physical artifact have been shown to increase trust and adoption rates, particularly in health-
sensitive contexts like asthma care.

Bloomy distinguishes itself from prior work by combining
air quality sensing with expressive, flower-like motion and
light, fostering a calming yet informative experience. It draws
inspiration from calm technology and tangible user interfaces,
creating a seamless blend of functionality and emotion. By
focusing on natural metaphors like blooming and wilting,
our design leverages embodied cognition to make invisible
phenomena like air pollution feel more real, accessible, and
actionable.

## III. DESIGN GOALS AND ASSUMPTIONS
Our design emphasizes tangibility and simplicity, aiming to
communicate air quality in an intuitive and non-intrusive way.
The physical form prioritizes high visibility, designed to be
seen clearly from across a room. For example, the device may
bloom or wilt like a flower, providing an immediate visual
metaphor for good or poor air quality, respectively.
We also wanted the device to serve as an aesthetically
pleasing, decorative object that fits naturally into a home
environment. Since air quality typically does not change
frequently, the device is designed to blend into the background
when conditions are normal, and gently capture attention when
something changes, functioning both as a passive sculpture and
an active alert system.

We operate under the assumption that users can interpret
metaphorical cues, such as associating a wilting flower with
poor air quality, or interpreting unnatural flower colors (e.g.,
bright blue, orange, or red) as signs of abnormality, and pink
as an indicator of clean air. These metaphors are chosen for
their emotional resonance and universal familiarity.

While the primary audience includes individuals with
asthma and their caregivers, who benefit from clear, ambient
cues without needing to check digital displays, the device is
also intended to appeal to anyone interested in monitoring
their air quality through a functional yet beautiful object in
their living space.

## IV. SYSTEM OVERVIEW
This system combines environmental sensing, metaphor-
driven actuation, and ambient feedback to create an intuitive
air quality monitor. The design integrates both hardware and
software components to produce a responsive, visible, and
decorative object.

### A. Hardware Components

#### Sensors: 
The system uses a suite of environmental sensors to monitor indoor air quality:
- Adafruit PMSA003I:  Measures PM2.5 and PM10 par-
    ticulate matter to detect airborne pollutants.
- Adafruit SCD-40:Measures carbon dioxide (CO 2 ) con-
    centration to assess ventilation and air freshness.
  
#### Actuators:
  - Stepper Motor:Controls the mechanical blooming and
     wilting of flower petals, serving as a tangible metaphor
     for air quality conditions.
  - NeoPixel Ring:Provides color-based visual feedback,
     using metaphorical color cues (e.g., pink = good,
     red/orange/blue = poor) to convey air quality at a glance.
#### Controller:
  - CLUE: Acts as the sensor hub. It reads data from con-
     nected sensors (PM2.5, CO 2 ), runs air quality evaluation
     logic, and communicates the results via Bluetooth.
  - Feather nRF52840: Serves as the main controller and
     Bluetooth receiver. It receives air quality status messages
     from the CLUE via Bluetooth and executes the appro-
     priate logic to control actuators. It is stacked directly on
     the CRICKIT FeatherWing, allowing it to command the
     attached hardware.
  - CRICKIT FeatherWing: Functions as the actuator
     driver board, connected to and controlled by the Feather.
     It interfaces with the NeoPixel (for color feedback) and
     stepper motor (for petal movement), executing commands
     passed from the Feather.

### B. Software Pipeline
#### Sensor Data Acquisition: 
Periodically collects data from all
sensors to capture current environmental conditions.

#### Threshold-Based Logic: 
Processes raw sensor inputs and compares them against predefined thresholds to determine
air quality status for both CO 2 levels and particulate matter (PM2.5/PM10).

#### Communication & Feedback Display:

- The Adafruit CLUE transmits the computed air quality
    status via Bluetooth to the Feather nRF52840, which
    handles actuator control.
- Detailed sensor metrics and air quality state are also
    displayed on the CLUE’s onboard screen, offering real-
    time feedback for users seeking more granular insight.

#### Actuator Control: 
Based on the current and previous air quality states:
- The stepper motor opens or closes the petals to metaphor-
ically represent air quality as a blooming or wilting
flower.
- The NeoPixel ring updates its color to reflect severity
levels, providing ambient visual cues (e.g., pink = good,
red/orange/blue = poor).

## V. FABRICATION AND PROTOTYPING PROCESS
### Sensor Part
This component is responsible for sensing indoor air quality
and transmitting the information to the output system. We
used the Adafruit PMSA003I to measure PM2.5 and PM
particulate matter, and the Adafruit SCD-40 to measure CO 2
levels. These sensors were connected to the Adafruit CLUE
board, which serves as the data collection and Bluetooth
transmission unit.

### Code Resources:
- Full project code: https://github.com/olivesmoo/bloomy
- Component testing: https://
    github.com/olivesmoo/bloomy/tree/
    6ee4889514b704a9ca89f710762d021b81b8aec

### Output Part: Physical Prototype

We initially explored a tulip-based design, but its upright
and fragile structure was not mechanically reliable. We pivoted
to a lotus-inspired form where the stem remains hidden,
enabling better stability and mechanical motion.
Design Concept and Mechanism:
The blooming mechanism was modeled in Tinkercad and
implemented using a rack-and-pinion system. A stepper motor
drives the gear (pinion), which translates rotation into vertical
linear motion to actuate the petals.

<img width="517" height="303" alt="image" src="https://github.com/user-attachments/assets/1776ed8d-91aa-4895-b840-446cb00baa50" />

Fig. 1. Rack and pinion CAD model (left) and stepper motor test with rack
prototype (right)

While the first 3D-printed prototype was successful in terms
of structure, some smaller elements lacked precision. These
tolerances prevented smooth blooming, leading us to iterate
on the design and explore alternative 3D models, including a
pre-designed lotus flower form.

### Mechanical Improvements:

- Added cable passthrough holes for NeoPixel wiring.
- Designed stem-to-motor couplings to prevent slippage.
- Introduced a weighted, stationary vase to avoid full
    assembly rotation.

### Final Assembly

The final prototype integrates the flower, electronics, and
structure into a single expressive unit. The NeoPixel sits at
the center of the flower and changes color based on air quality
levels. The stepper motor drives blooming/wilting via vertical
motion, coordinated through Bluetooth communication.

### Electronics and Control Logic

We used the Feather nRF52840 microcontroller and Crickit
FeatherWing to control the actuators. The control system
listens for Bluetooth messages from the CLUE board and
responds based on sensor data.

### Behavioral Logic:

- Default flower state is closed.
- If air quality is good:

<img width="592" height="602" alt="image" src="https://github.com/user-attachments/assets/3a27bf38-e959-448c-b2f1-170500d539c5" />

Fig. 2. Bloomy prototype in different bloom states with multicolor LED
feedback

- LED turns pink.
- Motor activates to bloom.
- If poor conditions are detected:
- LED changes to yellow (PM2.5), blue (CO 2 ), or red
(both).
- If previously open, flower closes.
Power Management:To reduce power load and thermal
strain, the system disables the stepper motor after 40 seconds
and inserts a sleep period before the next actuation cycle.


This design and fabrication process exemplifies the iterative
development required to merge aesthetics, motion, and sensor
feedback into a tangible, expressive interaction.

## VI. EVALUATION
### Functional Tests of Each Sensor
We conducted individual functional tests for each sensor
to verify accurate data transmission and responsiveness. The
Bluetooth-connected air quality sensor was evaluated under
a variety of environmental conditions to observe how it responded to changes in PM2.5 and CO 2 levels.

For example, in the MakerLab, where many physical components are being actively cut, sanded, and assembled, the
sensor consistently reported elevated PM2.5 levels. This result
aligned with expectations, given the abundance of particulate
matter in the space. In another test, we placed the sensor in
a small, enclosed room with four people present. The CO 2
readings increased significantly, reflecting reduced air circulation and increased carbon dioxide from human respiration.
Additionally, we performed a controlled test by manually
exhaling onto the sensor.

### Petal Movement Responsiveness to Thresholds

The blooming and closing motions of the flower were
directly tied to real-time air quality thresholds. When the
sensor detected favorable conditions, the stepper motor reliably
actuated the blooming mechanism, and the NeoPixel ring
shifted to a soft pink hue, signaling clean air. Conversely,
when poor air quality was detected, such as elevated PM2.5 or
CO 2 levels, the flower retracted, and the LED color changed
accordingly to reflect the specific pollutant.

While the system generally responded as intended, it occasionally encountered mechanical issues due to power limita-
tions. Specifically, when both the stepper motor and the LED
ring were active simultaneously, the motor sometimes failed to
complete its full rotation. This incomplete actuation resulted
in the flower not fully opening or closing. These power-related
issues will be discussed further in theChallengessection.

## VII. CHALLENGES AND LESSONS LEARNED
### Mechanical Noise

One unexpected challenge was the noise produced by
the stepper motor during operation. While the motor performed reliably in terms of actuation, the mechanical sound
generated—particularly during the blooming and closing actions—was noticeably loud. This detracted from the intended
calming and organic aesthetic of the flower, which was
designed to subtly reflect environmental quality in a home
setting. Future versions may explore quieter motor alternatives
or dampening techniques to preserve the ambient nature of the
device.

### Power Constraints and Actuation Reliability

Another significant challenge was the power distribution
between the stepper motor and the NeoPixel LED ring.
Both components demand relatively high and stable current.
When operated simultaneously, we observed intermittent performance issues, including incomplete rotations of the stepper
motor and erratic LED behavior. The motor, in particular,
would sometimes stall or fail to complete the blooming cycle,
resulting in partially open or stuck petals.
To mitigate this, we implemented a cooldown strategy:
after every actuation, the motor is released and given a rest
period before the next command is issued. While this improved
reliability slightly, it did not eliminate the problem entirely.
These symptoms suggest that a more robust power management strategy—such as separate power sources or capacitor
buffering—may be required in future iterations.

### Integration Complexity

Although each subsystem—the sensors, LED ring, and
motor—functioned correctly in isolation, integrating them
revealed unforeseen interactions. Most issues stemmed from
shared power constraints, timing mismatches, and communication delays over Bluetooth. This highlighted a key lesson:
individual component success does not equate to system-
level reliability. Designing for integration from the beginning, including thorough system-level testing and mocking communication flows, would have mitigated some of these issues
earlier in the process.

### Other Implementation Issues
Beyond the core technical challenges, we also faced mechanical design constraints. The routing of wires through the
stem, maintaining structural stability, and aligning the servo
with the flower mechanism required multiple redesigns and
reprints. Furthermore, limited access to high-resolution 3D
printing impacted the precision of delicate parts, occasionally
causing assembly misalignments.

### Reflections and Validations
Despite the above difficulties, our foundational design assumptions were largely validated. Bloomy’s core
metaphor—using expressive motion and ambient lighting to
communicate air quality—proved to be both feasible and
engaging. The metaphor of a blooming flower for clean air
and wilting for poor conditions resonated with users during
informal demonstrations, reinforcing our belief in the value of
tangible, ambient feedback for health-related awareness.
These experiences taught us the importance of designing
with both emotional resonance and technical feasibility in
mind. Our work supports the idea that tangible computing
systems, when carefully integrated, can provide accessible and
meaningful interaction paradigms for sensitive domains such
as asthma management.


## VIII. CONCLUSION
Bloomy transforms air quality monitoring into a gentle,
beautiful interaction. Rather than relying on numeric data,
mobile notifications, or app-based graphs, it leverages tangible
metaphors—light and motion—to intuitively alert users to
changes in their environment. By blooming in clean air and
wilting in poor conditions, Bloomy reduces the cognitive
load typically associated with interpreting environmental data,
making it especially accessible for asthma sufferers, children,
and the elderly.

Our prototype demonstrates that ambient, emotionally resonant feedback can increase engagement and promote proactive behavior without requiring constant user attention. The
seamless integration of sensors, wireless communication, and
expressive actuation bridges the gap between utility and
aesthetics—making health-relevant information feel natural,
visible, and meaningful in a home context.

Despite technical hurdles such as mechanical noise, power
distribution issues, and integration complexity, the core design
metaphor proved both functional and effective. Our evaluation
suggests that Bloomy’s flower-like behavior is not only legible
to users but also appreciated as an emotionally expressive
companion. The process reaffirmed that early system-level
testing and iterative prototyping are crucial in developing
tangible, interactive systems.

Looking ahead, Bloomy lays the groundwork for future
health-monitoring devices that are ambient, decorative, and emotionally aware. Future iterations may include quieter ac-
tuation, adaptive behavior based on user habits, multi-sensor
fusion for broader environmental insight, and long-term deployment studies to evaluate behavioral impact. We believe
Bloomy’s principles can inspire a new generation of tangible
interfaces that democratize access to environmental awareness
and transform how we experience and respond to invisible
health risks in our everyday spaces.


https://github.com/user-attachments/assets/6e7e981a-f225-4bc3-8fbe-43f2d652eb45

Fig. 3. Bloomy prototype displaying its response to good air quality

## REFERENCES

[1] California Air Resources Board, ”Air pollution and respiratory health.”
[Online]. Available: http://www.arb.ca.gov/
[2] Atmotube PRO. [Online]. Available: https://atmotube.com/atmotube-pro
[3] S. Kim and E. Paulos, ”inAir: Measuring and visualizing indoor air
quality,” inProc. Ubicomp, 2009.
[4] S. Kim and E. Paulos, ”InAir: Sharing indoor air quality measurements
and visualizations,” inProc. CHI, 2010.
[5] G. Wong-Parodi, M. B. Dias, and M. Taylor, ”Effect of using an indoor
air quality sensor on perceptions...,”JMIR mHealth and uHealth, vol.
6, no. 3, 2018.
[6] X. Zhou and V. Sampath, ”Effect of air pollution on asthma,”Annals of
Allergy, Asthma & Immunology, vol. 132, no. 2, 2024.

