x = 0:0.01:1;
figure(1)
filename = 'testnew51.gif';
for n = 1:0.5:5
      y = x.^n;
      plot(x,y)
      drawnow
      frame = getframe(1);
      im = frame2im(frame);
      [imind,cm] = rgb2ind(im,256);
      if n == 1;
          imwrite(imind,cm,filename,'gif', 'Loopcount',inf);
      else
          imwrite(imind,cm,filename,'gif','WriteMode','append');
      end
end