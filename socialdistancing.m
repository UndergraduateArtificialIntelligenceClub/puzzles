%% Determines the best starting configuration
% Justin Stevens
% June 1st, 2020

%% preliminary
close all
clear
clc
%% length of the bar
long=25;
gap=6;
% best length found so far
bestL=0;
bestF=0;
bestIC=[];

colorD=distinguishable_colors(long);
%% iterate over all the possible seats
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
    
    %% scatter y-coordinates
    vec=zeros(L, 1);
    positions=[1:L];
    vec(positions)=i;
    sz=linspace(125, 25, L);
    scatter(IC(1:L), vec, sz, colorD(i, :), 'filled');
    hold on;
    %% update if it's better
    if(L>bestL)
        bestL=L;
        bestF=i;
        bestIC=IC;
    end 
end 

vec=zeros(bestL, 1);
positions=[1:bestL];
vec(positions)=bestF;
sz2=linspace(225, 125, bestL);
scatter(bestIC(1:bestL), vec, sz2, colorD(bestF, :), 'p');

str=sprintf('Plot of Seating Configurations for a Table of Length %d and Gap %d', long, gap);
title(str);
xlabel("Seat Configuration");
ylabel("Location of First Person");