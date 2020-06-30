clear all; close all; clc;
%% ************************ QEV 1 PARAMETERS ******************************
% meq = equivalent mass, car+driver

% mv = vehicle mass(kg)
% Ro = rolling resistance coefficient
% L = wheelbase (axel to axel length)
% alpha = road gradient (0 for flat ground)
% A, B = longitudinal distance between front and rear axel to the centre of gravity 
% g = gravity

% Pair =  density of air kg/m^3
% Cd = Drag coefficient 
% Af = Frontal area
% V = Velocity
% Vair = Velocity of air (opposite direction to V)

% T = torque
% zetaI = 
% zetaMG = 
% zeta0 = ratio from engine to wheel
% n = efficiency
% rw = Wheel radius

mv = 310; % kg 

meq = mv + 70; %kg

Ro = 0.02; % found on https://hpwizard.com/tire-friction-coefficient.html, formula tires, had the same coefficient of friction so assumed correct/reasonable estimation
L = 1.530; % m
alpha = 0; % degrees
A = 0.6*L; % m
B = 0.4*L; % m
g = 9.81; % m/s^2

Pair = 1.1839; % kg/m^3
Cd = 0.8; % no units
Af = 0.765; % m^2
Vair = 0; % m/s

zeta0 = 4.5; % gear ratio
n = 0.8439; % efficiency, percentage assuming 0.97 gearbox, 0.87 motor
rw = 0.414/2; % m 0.4141; %

%% ************************** Constants ***********************************
kiloConvert = 1000;
hourConvert = 3600;

%% ************************ Calculations **********************************
% road load equation:
% meq * a = Ftrac - Faero - Frf - Frr - Fgrad
% Ftrac: Tractive force
% Faero: Aerodynamic force, drag
% Frf:   Front rolling resistance
% Frr:   Rear rolling resistance
% Fgrad: Gradient resistance, not needed due to relativel flat track

% VTest = 0:0.1:28;
% TTest = 0.1 .* ones(1, length(VTest));
% ATest = 0.1 .* ones(1, length(VTest));
% 
% time = TTest;
% V = VTest;
% accel = ATest;

TimeData = load('timeInterval.mat');
time = TimeData.time;

Velocity = load('speed.mat');
V = Velocity.speed;

Acceleration = load('longitudinalAcceleration.mat');
accel = Acceleration.LongAcceleration;

Frr = Ro * mv * g * cos(alpha) * (B/L);
Ffr = Ro * mv * g * cos(alpha) * (A/L);
Faero = 0.5 .* Pair .* Cd .* Af .* (V-Vair).^2;

% Ftrac = ( T * zeta0 * n ) / rw;

Ftrac = ( meq .* accel ) + Faero + Ffr + Frr; % Tractice Force

T = (( Ftrac .* rw ) ./ ( zeta0 .* n )) * 4; % Torque

Wn = V ./ rw; % Angular Velocity

Power = zeros(1, length(time));

for i = 1:length(T)
    Power(i) = T(i)*Wn(i); % Power at the wheels
%     if T(i) >=0
%         Power(i) = T(i)*Wn(i);
%     else
%         Power(i) = T(i)*Wn(i)*0.5;
%     end   
end

posEnergy = zeros(1, length(time));
energy = zeros(1, length(time));

for i = 2:length(time)
    energy(i) = energy(i-1) + Power(i).*time(i); % Energy used
    
    posPower = Power(i); % Total power used
    if (posPower<=0)
        posPower = 0; 
    end
    
    posEnergy(i) = posEnergy(i-1) + posPower.*time(i); % want only positive values to be returned, 0 for negative values
end

fprintf('Average power at wheel (absolute value):    %.2f kW\n\n', mean(abs(Power))/(kiloConvert*4))
fprintf('Average Torque at wheel (absolute value):    %.2f Nm\n\n', mean(abs(T))/4)

fprintf('Average power at wheel full car (absolute value):    %.2f kW\n\n', mean(abs(Power))/kiloConvert)
fprintf('Average Torque at wheel full car (absolute value):    %.2f Nm\n\n', mean(abs(T)))
% 
% TotalPower = (sum(Power)*((sum(time)/3600))/1000);
% 
% fprintf('Total power used: %.2f kW\n\n', TotalPower)

timePlot = zeros(1, length(time));
timePlot(1) = time(1);

for i = 2:length(time)
    timePlot(i) = timePlot(i-1)+time(i);
end
%% NICKS PART
% When acceleration is negative, the car is braking. Find all points when
% this is occuring
ind = zeros(1,length(accel));
for n = 1:length(accel)
   if accel(n) < 0
       ind(n) = n;
   else
       ind(n) = 0;
   end
end

% Match this to those time intervals when braking is occuring
timeplot = timePlot;
for n = 1:length(timePlot)
    if ind(n) == 0
        timeplot(n) = 0;
    end
end

% Assuming 87% efficiency for the motors, find the power input to the
% motors
n_motor = 0.87;
P_motor = mean(abs(Power))*0.87; % This will be energy delivered back to the motors

% System efficiency is cruical for this. Assume the system is 50% efficient
P_batt = P_motor*0.5;

% When timeplot is not zero, power is being sent back. Perform this
% calculation
for i = 1:length(timePlot)
    if timeplot(i) == 0
        Energy(i) = posEnergy(i) - P_batt; % Is this right? Watts to Watt seconds? Also feel free to change posEnergy and energy
    end
end


%% END OF NICKS PART

figure()
hold on
plot(timePlot, T)
title('Torque Plot for QEV1 at the Wheel')
ylabel('Torque (Nm)')
xlabel('Time (s)')
hold off

figure()
hold on 
plot(timePlot, energy/(kiloConvert*hourConvert), 'b')
plot(timePlot, posEnergy/(kiloConvert*hourConvert), 'r')
plot(timePlot(1:length(Energy)), Energy/(kiloConvert*hourConvert), 'g')
title('Energy Plot for QEV1')
xlabel('Time (s)')
ylabel('Energy (kWh)')
legend('energy', 'positive energy', 'adjusted energy')
hold off

figure()
hold on 
plot(V, Ftrac)
title('Road Load Curve')
ylabel('Force (N)')
xlabel('Speed (m/s)')
hold off

figure()
hold on 
plot(V, Power./kiloConvert)
title('Used Power vs Increasing Velocity')
ylabel('Power (kW)')
xlabel('Speed (m/s)')
hold off

fprintf('Used Energy in Simulated Race:   %.2f kWh\n', posEnergy(end)/(kiloConvert*hourConvert)) % convert Ws to kWh
fprintf('Total Simulation Time:     %.2f seconds\n\n', timePlot(end))

raceTime = 25; % time in minutes the the race goes for

enduEnergy = posEnergy(end)/(kiloConvert*hourConvert) * ((raceTime/60)/(timePlot(end)/3600)); % convert Ws to kWh, multiply by ratio of race time (hours) to sim time (hours)
fprintf('Expected Used Energy in Endurance Race:    %.2f kWh\n', enduEnergy)
fprintf('Total Race Time:   %.2f minutes\n\n', raceTime)