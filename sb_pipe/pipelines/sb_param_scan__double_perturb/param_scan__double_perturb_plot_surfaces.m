% This file is part of sb_pipe.
%
% sb_pipe is free software: you can redistribute it and/or modify
% it under the terms of the GNU General Public License as published by
% the Free Software Foundation, either version 3 of the License, or
% (at your option) any later version.
%
% sb_pipe is distributed in the hope that it will be useful,
% but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
% GNU General Public License for more details.
%
% You should have received a copy of the GNU General Public License
% along with sb_pipe.  If not, see <http://www.gnu.org/licenses/>.
%
% $Revision: 3.0 $
% $Author: Piero Dalle Pezze $
% $Date: 2015-07-7 23:14:32 $

% This script generates 2D and 3D plots of a double perturbation, for each time point 
% dataset contained in project/simulations/dp_datasets_dir. 
% The output will be stored in project/simulations/folderout

% FOLDERIN PATTERN NAME: SPECIES1_SPECIES2_data
% FOLDEROUT PATTERN NAME: SPECIES1_SPECIES2_plots


% this script requires param_scan__double_perturb_extract_timepoints.sh



disp('Script for generating 2D and 3D plots');
fprintf('\n');


dstruct = dir(fullfile(dp_datasets_dir,'/*__tp_*.csv'));
names = {dstruct.name};
maxlen = max(cellfun(@length, names));
padname = @(s) sprintf(['%0' num2str(maxlen) 's'], s);
namesPadded = cellfun(padname, names, 'UniformOutput', false);
[~, sortOrder] = sort(namesPadded);
dstruct = dstruct(sortOrder);

for i = 1:length(dstruct) 
%for i = 10:10 

    filein = dstruct(i).name;
    disp(['Reading file ', char(filein)]);

    % load file
    A = importdata([dp_datasets_dir, '/', filein], '\t', 1);
    [nrows, ncols] = size(A.data()); 

    % read header information
    xheader = A.colheaders(1,1);
    yheader = A.colheaders(1,2);

    % Set the values for the two species which are perturbed
    X = [];
    Y = [];
    param_scan__double_perturb_max_value_first_species = 90;
    param_scan__double_perturb_max_value_second_species = 90;
  
    switch param_scan__double_perturb_type_first_species
    case 'inhibition' 
        param_scan__double_perturb_max_value_first_species = 90;
    case {'overexpression', 'mixed'}
        param_scan__double_perturb_max_value_first_species = 250;
    otherwise
        warning('Unexpected perturbation type! Default value is inhibition');
    end
    X = [0:param_scan__double_perturb_max_value_first_species/param_scan__double_perturb_intervals_first_species:param_scan__double_perturb_max_value_first_species];    

    switch param_scan__double_perturb_type_second_species
    case 'inhibition' 
        param_scan__double_perturb_max_value_second_species = 90;
    case {'overexpression', 'mixed'}
        param_scan__double_perturb_max_value_second_species = 250;
    otherwise
        warning('Unexpected perturbation type! Default value is inhibition');
    end
    Y = [0:param_scan__double_perturb_max_value_second_species/param_scan__double_perturb_intervals_second_species:param_scan__double_perturb_max_value_second_species];     
    
    
    
    
    % Print information for debugging
    disp(char(xheader));     
    %disp(transpose(X));   
    disp(char(yheader));     
    %disp(transpose(Y));       

    %disp(size(X));
    %disp(size(Y));
    
    %header labels editing
    xheader=strrep(char(xheader), '_', '-');
    yheader=strrep(char(yheader), '_', '-');    
    xheader=strrep(char(xheader), '-percent', '');
    yheader=strrep(char(yheader), '-percent', '');
    xheader=strrep(char(xheader), 'ext-interv-', '');
    yheader=strrep(char(yheader), 'ext-interv-', '');     
    
    
    folderout=[dp_dir, '/', perturbed_species, param_scan__double_perturb_suffix_plots_folder, '/'];
    disp([folderout]);    
    [s,mess,messid] = mkdir(folderout);

    plotfontname='Arial';

    for k = (4:ncols)
    %for k = (16:16)
    
        % extract the vector Z and compute the matrix matZ
        Z = A.data(:,k);
        %disp(Z);
        zheader = A.colheaders(1,k);
        zheader = strrep(char(zheader), '_', '-');
        matZ=reshape(Z,param_scan__double_perturb_intervals_first_species+1,param_scan__double_perturb_intervals_second_species+1);       
        %disp(matZ);
        %disp(size(matZ));
        
        fprintf(['Generating plots for z=', char(zheader), '\n']);
	%mesh(X,Y,matZ); % wireframed grid-based 3d plot
	% Draw a surface and removes the wireframe grid
	surf(X,Y,matZ,'EdgeColor','none','LineStyle','none','FaceLighting','phong');
	
        if strcmp(param_scan__double_perturb_plots_2D_pub,'true')        
	    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	    % 2D data plotting and plot annotation (publication)
	    az = 0;
	    el = 90;
	    view(az, el);
	    colorbar('location','eastoutside','fontname',plotfontname,'FontSize',14,'FontWeight','bold','LineWidth',2);
	    %set(gca,'ActivePositionProperty','outerposition'); 
	    set(gcf,'Position',[100 80 800 600]);
	    set(gca,'Units','pixel');   
	    set(gca,'Position',[150 100 400 350]);  
	    xlabel([char(xheader),' (%)'],'fontname',plotfontname,'FontSize',25,'FontWeight','bold');
	    ylabel([char(yheader),' (%)'],'fontname',plotfontname,'FontSize',25,'FontWeight','bold'); 
	    title(char(zheader),'fontname','Arial','FontSize',30,'FontWeight','bold');
	    fileout = ['pub_2Dplot_' char(xheader) '_' char(yheader) '_' char(zheader) '_day' num2str(i-1)];
	    grid off;   
	    axis([0 param_scan__double_perturb_max_value_first_species 0 param_scan__double_perturb_max_value_second_species]);	    
	    set(gca, 'Box','on','TickDir','out','TickLength',[.01 .01], 'XMinorTick', 'off', 'YMinorTick', 'off');
	    set(gca,'fontname',plotfontname,'fontsize',10,'FontWeight','bold','LineWidth',2);
	    %saveas(gcf,[folderout, '/', fileout,'.fig'],'fig');    
	    print(gcf,'-dpng','-r300',[folderout, '/', fileout,'.png']);
	end

        if strcmp(param_scan__double_perturb_plots_3D,'true')
	    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
	    % 3D data plotting and plot annotation
	    az = -40;
	    el = 40;
	    view(az, el);
	    colorbar('location','eastoutside','fontname',plotfontname,'FontSize',12,'FontWeight','bold','LineWidth',2);	    
	    set(gcf,'Position',[100 80 800 600]);
	    %change the position of the plot
	    set(gca,'Units','pixel');   
	    set(gca,'Position',[150 100 400 350]);
	    xlabel([char(xheader),' (%)'],'fontname',plotfontname,'FontSize',12,'FontWeight','bold');
	    ylabel([char(yheader),' (%)'],'fontname',plotfontname,'FontSize',12,'FontWeight','bold'); 
	    zlabel(char(zheader),'fontname',plotfontname,'FontSize',12,'FontWeight','bold');
	    % save figure (gcf means "get current figure")
	    fileout = ['src_3Dplot_' char(xheader) '_' char(yheader) '_' char(zheader) '_day' num2str(i-1)];
	    grid on;   
	    axis([0 param_scan__double_perturb_max_value_first_species 0 param_scan__double_perturb_max_value_second_species]);
	    set(gca, 'Box','off','TickDir','out','TickLength',[.01 .01],'XMinorTick','off','YMinorTick','off');
	    set(gca,'fontname',plotfontname,'fontsize',10,'FontWeight','bold','LineWidth',2);
	    %saveas(gcf,[folderout, '/', fileout,'.fig'],'fig');    
	    print(gcf,'-dpng','-r300',[folderout, '/', fileout,'.png']);   
        end        
        
    end % end for
    fprintf('\n');
end % end for
