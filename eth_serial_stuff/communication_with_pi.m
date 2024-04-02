

pyrunfile('ssh_reset_eth.py');
disp('reset done')
input = ['rp_listen_write_copy.py', ' ', 'V1,1000'];
pyrunfile(string(input));
pyrunfile('ssh_reset_eth.py');
disp('reset done')


% 
% for i = 1:36
%     pyrunfile('ssh_reset_eth.py');
%     disp('reset done')
%     input = ['rp_listen_write_copy.py', ' ', 'V1,', num2str(i)];
%     pyrunfile(string(input));
%     pyrunfile('ssh_reset_eth.py');
%     disp('reset done')
%     pause(5)
% end