clear;
clc;
close all;

% Number of experiments
N = 3;

% Store estimated time constants
a = zeros(N,1);

figure;
hold on;
grid on;

for i = 1:N

    % Load experiment data
    filename = sprintf('run%d.txt', i);
    data = readmatrix(filename);

    t = data(:,1);
    y = data(:,2);

    % Set time origin to first measurement
    t = t - t(1);

    % Initial parameter estimates
    y0 = y(1);
    x = y(end);
    a0 = 10;

    % Model parameters:
    % p(1) = initial temperature
    % p(2) = final temperature
    % p(3) = log(time constant)
    model = @(p,t) p(1) + ...
        (p(2)-p(1)) .* (1-exp(-t/exp(p(3))));

    % Sum of squared errors
    error = @(p) sum((y-model(p,t)).^2);

    % Fit exponential response
    p0 = [y0, x, log(a0)];
    p = fminsearch(error, p0);

    % Extract time constant
    a(i) = exp(p(3));

    % Plot measured data
    plot(t, y, 'o', 'DisplayName', ...
        sprintf('Run %d Data', i));

    % Plot fitted response
    t_fit = linspace(0,max(t),500);
    y_fit = model(p,t_fit);

    plot(t_fit,y_fit,'-', 'LineWidth',1.5, ...
        'DisplayName',sprintf('Run %d Fit',i));

    fprintf('Run %d: a = %.4f seconds\n',i,a(i));

end

xlabel('Time (s)');
ylabel('Temperature (°C)');

% Calculate statistics
a_mean = mean(a);
a_std = std(a);

% 90% confidence interval
n = length(a);
t_critical = 2.920;

margin = t_critical * a_std / sqrt(n);

CI_lower = a_mean - margin;
CI_upper = a_mean + margin;

% Display results
fprintf('\n--- Thermal Time Constant Results ---\n');

fprintf('Mean a = %.4f seconds\n', a_mean);
fprintf('Standard deviation = %.4f seconds\n', a_std);

fprintf('90%% Confidence Interval:\n');
fprintf('[%.4f, %.4f] seconds\n', CI_lower, CI_upper);