%% Determines the best starting configuration
% Justin Stevens
% June 1st, 2020

%% preliminary
close all
clear
clc
%% length of the bar

% best length found so far
gap=3;
colorD=distinguishable_colors(40);
%% iterate over all the possible seats
for long=51:100
    bestL=0;
    bestF=0;
    bestIC=[];
    for i=1:long
        IC=[i];
        bestV=gap;
        while(bestV>=gap)
            [bestI, bestV]=gen_move(IC, long);
            if(bestI && bestV>=gap)
                IC=[IC, bestI];
            end 
        end
        %% find length of best iteration
        L=length(IC);
        %% update if it's better
        if(L>bestL)
            bestL=L;
            bestF=i;
            bestIC=IC;
        end 
    end 
    %% scatter y-coordinates
    if(bestL==ceil(long/gap))
        fprintf("%d ", long);
        scatter(long, bestL, 100, 'filled', 'p');
        hold on;
    else
        scatter(long, bestL, 42, 'filled');
        hold on;
    end
end
str=sprintf('Plot of Maximum People Seated for Gap %d', gap);
title(str);
xlabel("Number of Seats");
ylabel("Max Number of People Seated");