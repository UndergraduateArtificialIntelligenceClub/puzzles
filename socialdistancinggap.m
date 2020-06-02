%% Determines the best starting configuration
% Justin Stevens
% June 1st, 2020

%% preliminary
close all
clear
clc
%% length of the bar

% best length found so far


num_list=[3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 24, 25, 26, 32, 33, 34, 35, 36, 37, 38, 40, 41, 42, 48, 49, 50, 64, 65, 66, 67, 68, 69, 70, 72, 73, 74, 80, 81, 82, 96, 97, 98];
colorD=distinguishable_colors(40);
%% iterate over all the possible seats
long=65;
for gap=2:long
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
        scatter(gap, bestL, 100, 'filled', 'p');
        hold on;
    else
        scatter(gap, bestL, 50, 'filled');
        hold on;
    end
end
str=sprintf('Plot of Maximum People Seated for Length %d', long);
title(str);
xlabel("Gap Size");
ylabel("Max Number of People Seated");