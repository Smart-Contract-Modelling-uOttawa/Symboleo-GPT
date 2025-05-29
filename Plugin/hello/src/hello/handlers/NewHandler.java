package hello.handlers;

import org.eclipse.core.commands.AbstractHandler;
import org.eclipse.core.commands.ExecutionEvent;
import org.eclipse.core.commands.ExecutionException;
import org.eclipse.ui.IWorkbenchWindow;
import org.eclipse.ui.handlers.HandlerUtil;
import org.eclipse.jface.dialogs.MessageDialog;
import org.eclipse.core.resources.*;
import java.io.*;

public class NewHandler extends AbstractHandler {

    private static final String CUSTOM_FILE_PATH = "C:\\Users\\Sahil\\Desktop\\Masters\\Final year Project\\Contracts\\errors.txt";
    private static final String PYTHON_SCRIPT_PATH = "C:\\Users\\Sahil\\Desktop\\Masters\\Final year Project\\Python\\Analyser.py";
    private static final String PYTHON_EXECUTABLE = "C:\\Users\\Sahil\\AppData\\Local\\Programs\\Python\\Python313\\python";

    @Override
    public Object execute(ExecutionEvent event) throws ExecutionException {
        try {
            IWorkbenchWindow window = HandlerUtil.getActiveWorkbenchWindowChecked(event);
            
            StringBuilder errorMessages = new StringBuilder();
            IMarker[] markers = ResourcesPlugin.getWorkspace().getRoot()
                    .findMarkers(IMarker.PROBLEM, true, IResource.DEPTH_INFINITE);

            for (IMarker marker : markers) {
                if (marker.getAttribute(IMarker.SEVERITY, IMarker.SEVERITY_INFO) == IMarker.SEVERITY_ERROR) {
                    String message = (String) marker.getAttribute(IMarker.MESSAGE);
                    String resourceName = marker.getResource().getName();
                    int lineNumber = marker.getAttribute(IMarker.LINE_NUMBER, -1);

                    errorMessages.append("File: ").append(resourceName)
                            .append(", Line: ").append(lineNumber)
                            .append(", Message: ").append(message)
                            .append("\n");
                }
            }

            saveErrorsToFile(errorMessages.toString());
            
            boolean proceed = MessageDialog.openConfirm(
                    window.getShell(), "Run Statistical Analyser", 
                    "Errors have been saved to: " + CUSTOM_FILE_PATH + "\n\nClick OK to run the Statistical Analyser.");
            
            if (proceed) {
                boolean scriptSuccess = runPythonScript();
                MessageDialog.openInformation(
                        window.getShell(), "Statistics Execution", 
                        scriptSuccess ? "✅ Statistics ran successfully!" : "❌ Statistics execution failed.");
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }
    
    private boolean runPythonScript() {
        try {
            Process runScript = new ProcessBuilder(PYTHON_EXECUTABLE, PYTHON_SCRIPT_PATH).start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(runScript.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
            int exitCode = runScript.waitFor();
            return exitCode == 0;
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
            return false;
        }
    }
    
    private void saveErrorsToFile(String content) {
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(CUSTOM_FILE_PATH))) {
            writer.write(content);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
