% License (GPLv3):
% This program is free software; you can redistribute it and/or modify
% it under the terms of the GNU General Public License as published by
% the Free Software Foundation; either version 2 of the License, or (at
% your option) any later version.
%
% This program is distributed in the hope that it will be useful, but
% WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
% GNU General Public License for more details.
%
% You should have received a copy of the GNU General Public License
% along with this program; if not, write to the Free Software
% Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
%
%
% $Revision: 1.0 $
% $Author: Piero Dalle Pezze $
% $Date: 2013-04-20 12:14:32 $
%
%

% This script generates 2D and 3D plots of a double perturbation, for each time point 
% dataset contained in project/simulations/folderin. 
% The output will be stored in project/simulations/folderout

% FOLDERIN PATTERN NAME: perturb_SPECIES1_SPECIES2_data
% FOLDEROUT PATTERN NAME: perturb_SPECIES1_SPECIES2_plots


% this script requires param_scan__dp_extract_timepoints.sh



% length(X) is 1201
% length(Y) is 1201
% length(Z) is 1201x1201




disp('Script for generating 2D and 3D plots');
fprintf('\n');

% path = 'SB_PIPE/projXXX/simulations/';
% folderin = './perturb_Mitophagy-MFN2_ROS_data/';
% folderin = './perturb_Akt_JNK_data/';
% folderin = './perturb_AMPK_mTORC1_data/';

dstruct = dir(fullfile(path, '/', folderin,'/*_tp_*.csv'));
names = {dstruct.name};
maxlen = max(cellfun(@length, names));
padname = @(s) sprintf(['%0' num2str(maxlen) 's'], s);
namesPadded = cellfun(padname, names, 'UniformOutput', false);
[~, sortOrder] = sort(namesPadded);
dstruct = dstruct(sortOrder);

for i = 1:length(dstruct) 
    filein = dstruct(i).name;
    disp(['Reading file ', char(filein)]);

    % load file
    A = importdata([path, '/', folderin, '/', filein], '\t', 1);
    [nrows, ncols] = size(A.data());
    X = A.data(1:1201,2); % 0:300 percent
    Y = A.data(1:1201,2);
    xheader = A.colheaders(1,1);
    yheader = A.colheaders(1,2);

    % header labels editing
    xheader=strrep(char(xheader), '_', '-');
    yheader=strrep(char(yheader), '_', '-');
    xheader=strrep(char(xheader), '-percent', '');
    yheader=strrep(char(yheader), '-percent', '');

    folderout=[path, '/perturb_',char(xheader),'_', char(yheader),'_plots'];
    [s,mess,messid] = mkdir([path, '/', folderout]);
    


    for k = (4:ncols)
            
        % extract the vector Z and compute the matrix matZ
        Z = A.data(:,k);
        zheader = A.colheaders(1,k);
        zheader = strrep(char(zheader), '_', '-');
        matZ=reshape(Z,1201,1201);

        disp(['Generating plots for ', char(zheader)]);

        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
        % 3D data plotting and plot annotation
        mesh(X,Y,matZ);
        set(gcf,'Position',[100 80 800 600]);
        %change the position of the plot
        set(gca,'Units','pixel');   
        set(gca,'Position',[100 80 550 450]);
        xlabel([char(xheader),' (%)'],'FontSize',16,'FontWeight','bold');
        ylabel([char(yheader),' (%)'],'FontSize',16,'FontWeight','bold'); 
        zlabel(char(zheader),'FontSize',16,'FontWeight','bold');
        % save figure (gcf means "get current figure")
        fileout = ['src_3Dplot_' char(xheader) '_' char(yheader) '_' char(zheader) '_day' num2str(i-1)];
        grid on;   
        set(gca,'XTick',0:50:300,'YTick',0:50:300);     
        set(gca,'XTickLabel',{'0','50','100','150','200','250','300'});
        set(gca,'YTickLabel',{'0','50','100','150','200','250','300'}); 
        set(gca, 'Box','off','TickDir','out','TickLength',[.01 .01],'XMinorTick','off','YMinorTick','off');
        set(gca, 'FontName','Arial','fontsize',14,'FontWeight','bold','LineWidth',3);
        %saveas(gcf,[folder,fileout,'.png'],'png');
        %saveas(gcf,[folder,fileout,'.fig'],'fig');    
        print(gcf,'-dpng','-r600',[path, '/', folderout, '/', fileout,'.png']);   
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % 2D data plotting and plot annotation (publication)
        az = 0;
        el = 90;
        view(az, el);
        colorbar('location','eastoutside','FontSize',14,'FontWeight','bold','LineWidth',3);
        %set(gca,'ActivePositionProperty','outerposition'); 
        set(gcf,'Position',[100 80 800 600]);
        set(gca,'Units','pixel');   
        set(gca,'Position',[150 120 400 350]);
        xlabel([char(xheader),' (%)'],'FontSize',30,'FontWeight','bold');
        ylabel([char(yheader),' (%)'],'FontSize',30,'FontWeight','bold'); 
        title(char(zheader),'FontSize',30,'FontWeight','bold');
        fileout = ['pub_2Dplot_' char(xheader) '_' char(yheader) '_' char(zheader) '_day' num2str(i-1)];
        grid off;   
        set(gca,'XTick',0:50:300,'YTick',0:50:300);     
        set(gca,'XTickLabel',{'0','50','100','150','200','250','300'});
        set(gca,'YTickLabel',{'0','50','100','150','200','250','300'}); 
        set(gca, 'Box','on','TickDir','out','TickLength',[.01 .01],'XMinorTick','off','YMinorTick','off');
        set(gca, 'FontName','Arial','fontsize',30,'FontWeight','bold','LineWidth',3);
        print(gcf,'-dpng','-r600',[path, '/', folderout, '/', fileout,'.png']);
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
        % 2D data plotting and plot annotation (screen)
        az = 0;
        el = 90;
        view(az, el);
        colorbar('location','eastoutside','FontSize',16,'FontWeight','bold','LineWidth',3);
        set(gcf,'Position',[100 80 800 600]);
        set(gca,'Units','pixel');   
        set(gca,'Position',[100 80 450 400]);
        xlabel([char(xheader),' (%)'],'FontSize',20,'FontWeight','bold');
        ylabel([char(yheader),' (%)'],'FontSize',20,'FontWeight','bold'); 
        title(char(zheader),'FontSize',24,'FontWeight','bold');
        fileout = ['scr_2Dplot_' char(xheader) '_' char(yheader) '_' char(zheader) '_day' num2str(i-1)];
        grid off;   
        set(gca,'XTick',0:50:300,'YTick',0:50:300);     
        set(gca,'XTickLabel',{'0','50','100','150','200','250','300'});
        set(gca,'YTickLabel',{'0','50','100','150','200','250','300'}); 
        set(gca, 'Box','on','TickDir','out','TickLength',[.01 .01],'XMinorTick','off','YMinorTick','off');
        set(gca, 'FontName','Arial','fontsize',18,'FontWeight','bold','LineWidth',3);
        print(gcf,'-dpng','-r600',[path, '/', folderout, '/', fileout,'.png']);

    end % end for
    fprintf('\n');
end % end for
