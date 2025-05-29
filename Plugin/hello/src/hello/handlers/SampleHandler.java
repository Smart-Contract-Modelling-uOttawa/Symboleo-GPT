package hello.handlers;


import org.eclipse.core.commands.AbstractHandler;
import org.eclipse.core.commands.ExecutionEvent;
import org.eclipse.core.commands.ExecutionException;
import org.eclipse.core.resources.*;
import org.eclipse.core.runtime.CoreException;
import org.eclipse.ui.IWorkbenchWindow;
import org.eclipse.ui.handlers.HandlerUtil;
import org.eclipse.jface.dialogs.MessageDialog;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.BufferedWriter;
import java.io.FileWriter;
import org.eclipse.jface.dialogs.InputDialog;
import org.eclipse.jface.dialogs.IInputValidator;
import org.eclipse.swt.widgets.Shell;

public class SampleHandler extends AbstractHandler {

    @Override
    public Object execute(ExecutionEvent event) throws ExecutionException {
        try {
            // Get the active workbench window
            IWorkbenchWindow window = HandlerUtil.getActiveWorkbenchWindowChecked(event);

            // Collect all errors from the workspace
            StringBuilder errorMessages = new StringBuilder();
            IMarker[] markers = ResourcesPlugin.getWorkspace().getRoot().findMarkers(IMarker.PROBLEM, true, IResource.DEPTH_INFINITE);

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

            // Attempt to find the .symboleo file in the workspace
//            StringBuilder contractContent = new StringBuilder();
            IWorkspace workspace = ResourcesPlugin.getWorkspace();
            IWorkspaceRoot root = workspace.getRoot();
//            
//            findSymboleoFile(root, contractContent);
            StringBuilder contractContent = new StringBuilder();
            // The location of the contract
            File customLocation = new File("C:\\Users\\Sahil\\Desktop\\Masters\\Final year Project\\Contracts\\meatsale"); // Replace with your actual path
            findSymboleoFile(customLocation, contractContent);


            // Display the errors and contract in a message dialog
            String messageToShow = errorMessages.length() > 0 ? "Errors are Extracted Successfully!" : "No errors found in the Problems view.";
            messageToShow += "\n\nContract Content:\n" + (contractContent.length() > 0 ? "Symboleo Contract found successfully": "No .symboleo file found.");
            
            // Combine errors and contract content
            String outputContent = "Errors:\n" + (errorMessages.length() > 0 ? errorMessages.toString() : "No errors found.") 
                    + "\n\nContract Content:\n" + (contractContent.length() > 0 ? contractContent.toString() : "No .symboleo file found.");

            // Save the content to a text file in the workspace
            saveToFile(root, outputContent);

            MessageDialog.openInformation(
                    window.getShell(),
                    "Problems View and Contract",
                    messageToShow
            );
            
            boolean hasErrors = errorMessages.length() > 0;
            boolean allSuccess = true; // Track if all executions succeed
            
            if (hasErrors) {
            	Shell shell = window.getShell();
                InputDialog inputDialog = new InputDialog(
                    shell, 
                    "Number of Executions", 
                    "Please enter the number of times to generate corrected contract:", 
                    "", 
                    new IInputValidator() {
                        @Override
                        public String isValid(String newText) {
                            try {
                                Integer.parseInt(newText); // Validate if input is a number
                                return null; // Valid input
                            } catch (NumberFormatException e) {
                                return "Invalid number. Please enter a valid integer.";
                            }
                        }
                    }
                );

                // Open the dialog and get user input
                if (inputDialog.open() == InputDialog.OK) {
                    String userInput = inputDialog.getValue();
                    int userNumber = Integer.parseInt(userInput);
//                for (int i = 0; i < userNumber; i++) {
                    boolean scriptSuccess = runPythonScript(userNumber);

                    if (!scriptSuccess) {
                        allSuccess = false;
                    }
//                }
                

                if (allSuccess) {
                    messageToShow += "\n\n Corrected contract generated successfully " + userNumber + " times!";
                } else {
                    messageToShow += "\n\n Failed to generate the corrected contract.";
                }
            } 
                else {
                messageToShow += "\n\n Failed to get the user input";
            }
            }
            else {
            	messageToShow += "\n\n No errors found. Skipping contract generation.";
            }

//            }
            // Show the final message in the UI
            MessageDialog.openInformation(
                    window.getShell(),
                    "Problems View and Contract",
                    messageToShow
            );
            
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }
    
    public void findSymboleoFile(File directory, StringBuilder contractContent) {
        if (directory == null || !directory.exists() || !directory.isDirectory()) {
            System.out.println("Invalid directory: " + (directory != null ? directory.getAbsolutePath() : "null"));
            return;
        }

        File[] files = directory.listFiles();
        if (files != null) {
            for (File file : files) {
                if (file.isFile() && file.getName().endsWith(".symboleo")) {
                    // Found a .symboleo file, read its content
                    try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
                        String line;
                        while ((line = reader.readLine()) != null) {
                            contractContent.append(line).append("\n");
                        }
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                } else if (file.isDirectory()) {
                    // Recursively search in subdirectories
                    findSymboleoFile(file, contractContent);
                }
            }
        }
    }
    
    private void saveToFile(IWorkspaceRoot root, String content) {
        try {
            // Create a file in the workspace root
            File outputFile = root.getLocation().append("workspace_output.txt").toFile();

            // Write content to the file
            try (BufferedWriter writer = new BufferedWriter(new FileWriter(outputFile))) {
                writer.write(content);
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private boolean runPythonScript(int iteration) {
        try {
            // Specify the correct Python binary
//            String pythonPath = "/usr/bin/python3"; // Change this to the correct Python path for MACOS
        	String pythonPath = "C:\\Users\\Sahil\\AppData\\Local\\Programs\\Python\\Python313\\python";

            // Check if OpenAI is installed
            Process checkOpenAI = new ProcessBuilder(pythonPath, "-c", "import openai").start();
            int checkExitCode = checkOpenAI.waitFor();

            // If OpenAI is missing, install it automatically
            if (checkExitCode != 0) {
                System.out.println("Installing OpenAI package...");
                Process installProcess = new ProcessBuilder(pythonPath, "-m", "pip", "install", "openai").start();
                installProcess.waitFor();
            }

            // Run the Python script
            String scriptPath = "C:\\\\Users\\\\Sahil\\\\Desktop\\\\Masters\\\\Final year Project\\\\Python\\\\LLM.py";
            Process runScript = new ProcessBuilder(pythonPath, scriptPath, String.valueOf(iteration)).start();

            BufferedReader reader = new BufferedReader(new InputStreamReader(runScript.getInputStream()));
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
         // Wait for process to complete
            int exitCode = runScript.waitFor();
//            runScript.waitFor();
            System.out.println("Python script executed successfully.");
         // Return true if script executed successfully (exit code 0)
            return exitCode == 0;
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
            return false; // Return false if an error occurs
        }
    }

}