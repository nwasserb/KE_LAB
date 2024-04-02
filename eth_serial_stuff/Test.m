
% test.m

% for i = 20:6000
%     pause(i)
%     var = i;
%     input = 'matlab_test.py ' + string(var);
%     pyrunfile(string(input));
% end

var = 5;
polarization = 'c';
port = 1238;
index = 0;
for i = 60:6000;
    if index == 5
        port = port + 4;
        index = 0;
    end
    % pause(i)
    var = i;
    disp(port)
    input = 'matlab_test.py ' + string(var) + ' ' + string(port);
    pyrunfile(string(input));
    index = index + 1;
end


% % Construct the command string
% command = ['matlab_test.py ', polarization, ' ', num2str(port)];
% 
% % Execute the command
% pyrunfile(command);
