fprintf('Precharge Calculations:\n')
%% Pre-Charge Circuit Component Parameteres %%
Vs = 30*3.3;
t = linspace(0, 500*1e-3, 1000);
C = 500*1e-6;
Tau = 100*1e-3;

% Using the RC circuit charge equation
% Vc = Vs.*(1-exp(-t./(R.*C)))
% Rearrange for R
% Let t = Tau where Tau is the time that the precharge will opperate for
% Let Vc = 99% of Vs when precharge finishes operation

R = (-Tau/(log(1-((0.99*Vs)/Vs)))/C);

fprintf('Recommended resistor value:                            %.2f Ohm\n', R)
%R = round(R/10)*10;
R = input('Using resistor value:                                  ');
%% Plots
Vc = Vs.*(1-exp(-t./(R.*C)));

Ic = (Vs-Vc)./R;
maxIc = max(Ic);
Pc = Vc.*Ic;
Pmax = max(Pc);

figure()
suptitle('Precharge Circuit Operational Characteristics')
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

fprintf('Max precharge current:                                 %.2f A\n', maxIc)
fprintf('Max power disipated:                                   %.2f W\n\n', Pmax)