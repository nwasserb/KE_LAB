close all;
clear all;

basis = ["H", "V", "D", "A", "L", "R"];
pa_1__port = serialport('COM8', 115200);         % PA Setting the Baud Rate
%pa_2__port = serialport('COM6', 115200);         % PA

for d1=1:6
    for d2=1:6
        coinc_mat(d1, d2) = measure_basis(pa_1__port, pa_2__port, basis(d1), basis(d2));
    end
end

coinc_vec = reshape(coinc_mat, 1, []);           % A row vector of 36 coincidence counts
fprintf('Coincedence count:');
display(coinc_vec)

%% PA Analysis
    function Coinc = measure_basis(port_1, port_2, x, y)
    writeline(port_1, "2");     % 2 is the setting 
    writeline(port_1, "c");     % c is the configuration 
    writeline(port_1, x);       % x,y is the polarization measurement
    
    input = 'matlab_test.py ' + string(y);
    pyrunfile(string(input))
    
    tacq = 30; % integration time
    %Start_offset = -1000; % start histogram offset
    %end_offset = 1000; % end histogram offset
    %start_coinc_bin = 955; % start coincidence sum offset

    % fiberloop
    Start_offset = 134500; % start histogram offset
    end_offset = 136500; % end histogram offset
    start_coinc_bin = 1060; % start coincidence sum offset    
    window = 21;
    end_coinc_bin = start_coinc_bin + (window-1); % end coincidence sum offset
    
    %%
    sp = ' ';
    site1name = 'a'; % a: Alice b: Bob
    site1ip = '10.0.3.5'; % FPGA IP address
    count_cmd = [pwd, '\main_count.exe']; % no change
    StartCMD = ['cmd_one.bat ', count_cmd, sp, site1ip, sp, num2str(tacq), sp, site1name]; % no change
    %%
    find_coinc = 1; % 0=Plot histograms; 1=Find coinc
    %% Coincidence counting command
    CoincCMD = ['main_coinc_mat.exe ', ... % no change
        num2str(Start_offset), ' ', ... % no change
        num2str(end_offset), ' ', ... % no change
        [site1name, '1'], ' ', ... % should be 1 for det 1
        [site1name, '2'], ' ', ... % should be 2 for det 2
        ];
    
    [~, ~] = system(StartCMD);
    pause(tacq+2);
    
    [~, cmdout] = system(CoincCMD);
    cmdout_data = strsplit(cmdout, ',');
    %%
    file_names = 'coinc_a1a2_'; % add the name of expected histograms. Change _a1a1_ to refelect the detectors
    %%
    % Define range locations
    max_sum = 0;
    max_file = '';
    max_hist = [];
    max_pos = 0;
    m_pos = 0;
    m_val = 0;
    values = [];
    if find_coinc == 1
        for i = 1:3
            data = csvread([file_names,num2str(i-2)]);
            values = data(3:end);
            [m_val,m_pos] = max(values);
            sum_values = sum(values(start_coinc_bin:end_coinc_bin));
            if sum_values > max_sum
                max_sum = sum_values;
                max_file = num2str(i-2);
                max_hist = values;
                max_pos = m_pos;
            end
        end
        % Display results
        fprintf('Max sum: %d\n', max_sum);
        fprintf('Associated file: %s\n', max_file);
        plot(max_hist,"lineWidth",3,'DisplayName',num2str(i-2))
        xlim([1 length(max_hist)])
        legend
    else
        figure;
        hold on;
        for i = 1:3
            data = csvread([file_names,num2str(i-2)]);
            values = data(3:end);
            plot(values,"lineWidth",3,'DisplayName',['PPS ffset: ' num2str(i-2)])
            [m_val,m_pos] = max(values);
            sum_values = sum(values(start_coinc_bin:end_coinc_bin));
            if sum_values > max_sum
                max_sum = sum_values;
                max_file = num2str(i-2);
                max_hist = values;
                max_pos = m_pos;
            end
        end
        xlim([1 length(max_hist)])
        legend
    end
    %%
    countA = str2double(cmdout_data{1});
    countB = str2double(cmdout_data{2});
    Acc = sum(values(1:window));
    Coinc = max_sum;
    
    fprintf('Det A: %d\tDet B: %d\tAcc: %d\tCoinc: %d \tPeak: %d\n',countA, countB, Acc, Coinc, max_pos);
    end