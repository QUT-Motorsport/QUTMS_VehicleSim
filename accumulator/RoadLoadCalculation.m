clear all; close all; clc;
%% ************************ QEV 1 PARAMETERS ******************************
% meq = equivalentMass

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

FoS = 1.05;
regen = 0.1;

totalMass = 380; % kg
cellWeight = 76; % g
cellsPack = 60; % int
packs = 12; % int
cellWeight = (cellWeight * cellsPack * packs) / 1000; % kg
driverWeight = 70; % kg

% 5.91kWh (6.47kWh actual) convergence at 59.28 kg 5% FOS 50% regen

% 5.65kWh (5.79kWh actual) convergence at 45.60 kg 0% FOS 50% regen
% 5.87kWh (6.24kWh actual) convergence at 57.46 kg 5% FOS 50% regen
% 5.95kWh (6.68kWh actual) convergence at 61.56 kg 10% FOS 50% regen ******
% 10.10kWh (10.69kWh actual) convergence at 98.50 kg 5% FOS 0% regen
% 7.45kWh (8.02kWh actual) convergence at 73.87 kg 5% FOS 30% regen

accumBox = 30; % kg, accumulator casing and hardware weight
vehicleMass = totalMass - driverWeight - cellWeight;
mv = vehicleMass + cellWeight; % kg, base weight of car not including driver
meq = totalMass; %kg equivalentMass

Ro = 0.02; % found on https://hpwizard.com/tire-friction-coefficient.html, formula tires, had the same coefficient of friction so assumed correct/reasonable estimation
L = 1.530; % m, wheel base
alpha = 0; % degrees, road slope
A = 0.6*L; % m
B = 0.4*L; % m
g = 9.81; % m/s^2, gravity

Pair = 1.1839; % kg/m^3, density of air
Cd = 0.68; % no units, 0.8 initial design, 1.6 potential
Af = 1.1; % m^2, frontal area, for car 0.21 m^2, 0.725 initial design
Vair = 0; % m/s, velocity of air

zeta0 = 4.5; % gear ratio
n = 0.8439; % efficiency, percentage assuming 0.97 gearbox, 0.87 motor
rw = 0.2032; % m, wheel radius

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

% VTest = [0:0.74:30.5, 30.5:-0.74:0];
% TTest = 0.1 .* ones(1, length(VTest));
% ATest = [7.4 .* ones(1, length(VTest)/2), -7.4 .* ones(1, length(VTest)/2)];
% 
% time = TTest;
% V = VTest;
% accel = ATest;

TimeData = load('timeInterval.mat'); 
time = TimeData.time; % time sample per velocity step % use this for your time steps, don't assume uniform steps as it isn't

Velocity = load('speed.mat');
V = Velocity.speed;
avgVelocity = mean(V);

Acceleration = load('longitudinalAcceleration.mat');
accel = Acceleration.LongAcceleration;

Frr = Ro * mv * g * cos(alpha) * (B/L);
Ffr = Ro * mv * g * cos(alpha) * (A/L);
Faero = 0.5 .* Pair .* Cd .* Af .* (V-Vair).^2;

% Ftrac = ( T * zeta0 * n ) / rw;

Ftrac = ( meq .* accel ) + Faero + Ffr + Frr;

T = (( Ftrac .* rw ) ./ ( zeta0 .* n ) .* 4);

Wn = V ./ rw;

Power = zeros(1, length(time));
truePower = zeros(1, length(time));
for i = 1:length(T)
    truePower(i) = T(i)*Wn(i);
    if T(i) >=0
        Power(i) = T(i)*Wn(i);
    else
        Power(i) = T(i)*Wn(i)*regen*n; % assuming 50% efficiency for regen, the regenerated power is then multiplied by the system efficiency to account for losses in the other systems
    end   
end

posEnergy = zeros(1, length(time));
energy = zeros(1, length(time));
trueEnergy = zeros(1, length(time));

for i = 2:length(time)
    energy(i) = energy(i-1) + Power(i).*time(i);
    trueEnergy(i) = trueEnergy(i-1) + truePower(i).*time(i);
    posPower = Power(i);
    if (posPower<=0)
        posPower = 0; 
    end
    
    posEnergy(i) = posEnergy(i-1) + posPower.*time(i); % want only positive values to be returned, 0 for negative values
end

fprintf('Average power at motor (absolute value):               %.2f kW\n', mean(abs(Power))/(kiloConvert*4))
fprintf('Average Torque at motor (absolute value):              %.2f Nm\n\n', mean(abs(T))/(4*4.5))

fprintf('Average power at wheel (absolute value):               %.2f kW\n', mean(abs(Power))/(kiloConvert*4))
fprintf('Average Torque at wheel (absolute value):              %.2f Nm\n\n', mean(abs(T))/4)

fprintf('Average power at wheel full car (absolute value):      %.2f kW\n', mean(abs(Power))/kiloConvert)
fprintf('Average Torque at wheel full car (absolute value):     %.2f Nm\n\n', mean(abs(T)))

fprintf('Max power at motor (absolute value):                   %.2f kW\n', max(abs(Power))/(kiloConvert*4))
fprintf('Max Torque at motor (absolute value):                  %.2f Nm\n\n', max(abs(T))/(4*4.5))

fprintf('Max power at wheel (absolute value):                   %.2f kW\n', max(abs(Power))/(kiloConvert*4))
fprintf('Max Torque at wheel (absolute value):                  %.2f Nm\n\n', max(abs(T))/4)

fprintf('Max power at wheel full car (absolute value):          %.2f kW\n', max(abs(Power))/kiloConvert)
fprintf('Max Torque at wheel full car (absolute value):         %.2f Nm\n\n', max(abs(T)))

% 
% TotalPower = (sum(Power)*((sum(time)/3600))/1000);
% 
% fprintf('Total power used: %.2f kW\n\n', TotalPower)

timePlot = zeros(1, length(time));
timePlot(1) = time(1);

for i = 2:length(time)
    timePlot(i) = timePlot(i-1)+time(i);
end

figure()
hold on
plot(timePlot, T)
title('Torque Plot for QEV1 at the Wheel')
ylabel('Torque (Nm)')
xlabel('Time (s)')
hold off

figure()
hold on 
plot(timePlot, posEnergy/(kiloConvert*hourConvert), 'r')
plot(timePlot, energy/(kiloConvert*hourConvert), 'b')
plot(timePlot, trueEnergy/(kiloConvert*hourConvert), 'g')
title('Energy Plot for QEV1')
xlabel('Time (s)')
ylabel('Energy (kWh)')
legend('energy 0% regen', 'energy 50% regen', 'energy 100% regen')
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

fprintf('Used Energy in Simulated Race:                         %.2f kWh\n', energy(end)/(kiloConvert*hourConvert)) % convert Ws to kWh
fprintf('Total Simulation Time:                                 %.2f seconds\n\n', timePlot(end))

raceTime = 25; % time in minutes the the race goes for

enduEnergy = energy(end)/(kiloConvert*hourConvert) * ((raceTime/60)/(timePlot(end)/3600)); % convert Ws to kWh, multiply by ratio of race time (hours) to sim time (hours)
fprintf('Expected Used Energy in Endurance Race:                %.2f kWh\n', enduEnergy)
fprintf('Total Race Time:                                       %.2f minutes\n\n', raceTime)

% figure()
% hold on 
% plot(timePlot, posEnergy/(kiloConvert*hourConvert)* ((raceTime/60)/(timePlot(end)/3600)), 'r')
% plot(timePlot, energy/(kiloConvert*hourConvert)* ((raceTime/60)/(timePlot(end)/3600)), 'b')
% plot(timePlot, trueEnergy/(kiloConvert*hourConvert)* ((raceTime/60)/(timePlot(end)/3600)), 'g')
% title('Energy Plot for QEV1')
% xlabel('Time (s)')
% ylabel('Energy (kWh)')
% legend('energy 0% regen', 'energy 50% regen', 'energy 100% regen')
% hold off

%% ******************** Battery Calculations ******************************
% Constants 
Vnom = 99; % Nominal Voltage of System
cellNom = 3.3; % Nominal Voltage of the cell
cellCap = 2.5; % cell capacity Ah
cellWeight = 0.076; % cell weight kg

% Conversion Rates
USD = 1.41;
EURO = 1.60;

cellPrice = 7.75*USD;

accumCap = (enduEnergy*kiloConvert*FoS)/Vnom;

parallelCells = ceil(accumCap/cellCap);
seriesCells = ceil(Vnom/cellNom);
totalCells = seriesCells*parallelCells;
totalWeight = totalCells*cellWeight;
totalCost = totalCells*cellPrice;

fprintf('Accumulator Capacity Required:                         %.2f Ah\n', accumCap)
fprintf('Actual Accumulator Capacity:                           %.2f Ah\n', parallelCells*cellCap)
fprintf('Actual Accumulator Energy:                             %.2f kWh\n', (seriesCells*cellNom)*(parallelCells*cellCap)/1000)
fprintf('Series Cells:                                          %d\n', seriesCells)
fprintf('Parallel Cells:                                        %d\n', parallelCells)
fprintf('Total Cells:                                           %d\n', totalCells)
fprintf('Total Weight:                                          %.2f kg\n', totalWeight)
fprintf('Total Cost:                                            $%.2f AUD\n\n', totalCost)

%% ************************** Enery Plots ****************************** %%
currentDraw = abs(Power)./Vnom; % Absolute current % Use this current for your calculations
timeTaken = zeros(1, length(time));
a = 1;
for i = 1:length(currentDraw)
    if currentDraw(i) >= 500
        timeTaken(a) = timeTaken(a)+time(i);
    else
        a = a+1;
    end
end

fprintf('Maximum time of peak current (>500 A):                 %.2f seconds\n', max(timeTaken(timeTaken>0)))
fprintf('Total time of peak current (>500 A):                   %.2f seconds\n', (sum(timeTaken)*((25*60)/sum(time)))/60)
fprintf('Peak current ratio:                                    %.2f %% \n\n', (sum(timeTaken)/sum(time))*100)

figure()
hold on
plot(timePlot, currentDraw)
xlabel('Time (s)')
ylabel('Current (A)')

Irms = rms(Power./Vnom);
IrmsDraw = rms(currentDraw);
Iavg = mean(Power./Vnom);
peakCurrent = max(Power./Vnom);
fprintf('Peak Current:                                          %.2f A\n', peakCurrent)
fprintf('RMS Current:                                           %.2f A\n', Irms)
fprintf('RMS Current Draw:                                      %.2f A\n', IrmsDraw)
fprintf('Average Current:                                       %.2f A\n\n', Iavg)

figure()
hold on
plot(timePlot, Power./Vnom, 'b')
P1 = plot(timePlot, Irms.*ones(length(timePlot), 1), 'r');
P2 = plot(timePlot, Iavg.*ones(length(timePlot), 1), '-g');
[PeakVal, idx] = max(Power./Vnom);
P3 = plot(timePlot(idx), PeakVal, '*k');
xlabel('Time (s)')
ylabel('Current (A)')
legend([P1, P2, P3], sprintf('RMS Current = %.2f', Irms), sprintf('Mean Current = %.2f', Iavg), sprintf('Peak Current = %.2f', max(Power./Vnom)))
axis([0 70 -600 950])


figure()
plot(timePlot, fftshift(fft(Power./Vnom))./34)

fprintf('Avergage Velocity:                                     %.2f km/h\n', avgVelocity*3.6)

fprintf('10%% power current draw:                                %.2f A\n', (max(abs(Power))*0.1)/(Vnom))
fprintf('30%% power current draw:                                %.2f A\n\n', (max(abs(Power))*0.3)/(Vnom))

run('PreChargeCalc.m')