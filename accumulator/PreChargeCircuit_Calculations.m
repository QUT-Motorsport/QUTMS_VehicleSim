fprintf('Precharge Calculations\n\n')
%% Pre-Charge Circuit Component Parameteres %%
% http://liionbms.com/php/precharge.php
% Define the desired precharge time, the precharge current reaches 1/e of
% it is initial value after time of : Tau = R*C ; assume Tau = 100ms
Tau = 100 * 1e-3;

% The current will be managable after a certain amount of time. that time
% is 5*Tau, so if the desired precharge time was 100ms and the load capcity
% 5Tau gives a capacitor charge of 99.3% 
% is 50000 uf, R is then equal to:
Load_capcity = 500*1e-6;
R = (Tau / (Load_capcity * 5)); 
fprintf('The Resistor Value Should be %4.2f ohms. \n', R);


% The Energy dissipated by the precharge resistor is E =
% (Load_capcity*v^2)/2 :
V = 30*3.3; % 27 cell in series
E = (Load_capcity * V^2)/2;
fprintf('The Energy Dissipated by the Precharge Resistor is %4.2f Joules. \n', E);

% The Power dissipated by the precharge  resistor during the precharge is
% the the energy over precharge time.
P = E/Tau;
fprintf('The Power Dissipated by the Precharge Resistor During the Precharge is %4.2f Watts \n',P);

% The instantaneoues power at the beginning of the precharge is :
p_instantaneous = V^2 /R;
fprintf('The Instantaneoues Power at the Beginning of the Precharge is %4.2f watts \n',p_instantaneous)

%% Plots
Vs = 30*3.3;
t = linspace(0, 500*1e-3, 1000);
C = Load_capcity;

Vc = Vs.*(1-exp(-t./(R.*C)));

Ic = (Vs-Vc)./R;
maxIc = max(Ic);
Pc = Vc.*Ic;

figure()
hold on
subplot(3, 1, 1)
plot(t, Vc, 'r')
ylabel('Voltage (V)')
subplot(3,1,2)
plot(t, Ic, 'b')
ylabel('Current (A)')
subplot(3,1,3)
plot(t, Pc, 'g')
xlabel('Time (s)')
ylabel('Power (W)')
hold off

fprintf('Max precharge current:     %.2f A\n\n', maxIc)