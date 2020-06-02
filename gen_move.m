function [bestI, bestV]=gen_move(IC, maxE)
%% Generates a best index for an initial configuration with max elements
% Justin Stevens
% June 1st, 2020

%% argument types
arguments
    IC (1, :) int64
    maxE int64
end

%% test to see if we can find a better value
bestI=0;
bestV=-1;
for i=1:maxE
    if(~ismember(i, IC))
        diff=min(abs(i-IC));
        if(diff>bestV)
            bestV=diff;
            bestI=i;
        end 
    end 
end  