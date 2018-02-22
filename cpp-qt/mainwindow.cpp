#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent), ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    this->setFixedSize(QSize(423, 417)); // Sets fixed size for window so its not resizable

    fileDialog = new QFileDialog(this);                     // Initialises QFileDialog object
    fileDialog->setFileMode(QFileDialog::ExistingFile);     // Allows user to only pick one file
    fileDialog->setNameFilter(tr("Excel Files (*.xlsx)"));  // Sets required file extension to .csv
    fileDialog->setViewMode(QFileDialog::Detail);           // Presents detailed view of files in file dialog
    fileDialog->setDirectory("C:/Users/<USER>/Documents");  // Sets initial directory to "Documents" for file dialog

}

MainWindow::~MainWindow()
{
    // Free memory
    delete ui;
}

void MainWindow::closeEvent(QCloseEvent *event)
{
    // Ask user if they really want to quit
    int result = QMessageBox::question(this, tr("GHS Voting: Quit"), tr("Are you sure you want to exit?"), QMessageBox::Yes, QMessageBox::Cancel);

    // Process their response
    if(result == QMessageBox::Yes)
        event->accept();
    else
        event->ignore();

}

void MainWindow::on_OpenFileButton_clicked()
{
    if(fileDialog->exec())                                      // Executes file dialog
        ui->FileName->setText(fileDialog->selectedFiles()[0]);  // Sets file line edit text to selected file's directory
}

// Processes click of the "Run" button, with respect to selected voting method
void MainWindow::on_RunButton_clicked()
{
    std::string message = "Have you ensured all data provided is correct? \n e.g. excel sheet names, filepath and integrity of the excel file (columns are correct, numbers are correct, no empty cells in candidate columns etc.) \n Failure to do so, can result in program failure, crashes etc.)";
    int ret = QMessageBox::warning(this, tr("User Warning"), tr(message.c_str()), QMessageBox::No | QMessageBox::Yes);

    if (ret == QMessageBox::Yes && filepathSet && sheetNameSet) {

        // Edit votefilepath so it does not contain backslashes which have double meanings
        for (int i = 0; i < votesFilePath.length(); i++)
            if (votesFilePath[i] == '\\')
                votesFilePath[i] = '/';

        // Create interface to vote_data_filepath.txt for writing
        QFile writeFile(writeFilePath);

        // Open write file with write-only rights and file type being text
        if(writeFile.open(QIODevice::WriteOnly | QIODevice::Text)) {
            // Clear file
            writeFile.resize(0);

            if (!newlineSet) {
                votesFilePath += " \n";
                newlineSet = true;
            }

            // Write filepath and sheetname and close
            writeFile.write(votesFilePath.toStdString().c_str());
            writeFile.write(sheetName.toStdString().c_str());
            writeFile.close();
        }
        else
            QMessageBox::critical(this, tr("Internal Error"), tr("Unable to open vote_data_filepath.txt"), QMessageBox::Ok); // Message to user in case of inability to open file

        // Run.bat starts the python IRV algorithm
        std::system("RunPython.bat");


        // Create interface to file where results are stored
        QFile readFile(resultsFilePath);

        // Strings to store results for captain and vice captain
        QString captain;
        QString cVotes;
        QString vice;
        QString vcVotes;
        QString tvCount;
        QString vavCount;

        // Open read file with read-only rights and file type being text
        if(readFile.open(QIODevice::ReadOnly | QIODevice::Text)) {
            // Interface to read text
            QTextStream inFile(&readFile);

            // Get text from file. readLine at end of reading, sets its view on the next line (no iteration required)
            captain = inFile.readLine();
            cVotes = inFile.readLine();
            vice = inFile.readLine();
            vcVotes = inFile.readLine();
            tvCount = inFile.readLine();
            vavCount = inFile.readLine();

            readFile.close();
        }
        else
            QMessageBox::critical(this, tr("Internal Error"), tr("Unable to open results.txt"), QMessageBox::Ok); // Message to user in case of inability to open file

        // Set the text in the results browser to results obtained from results.txt
        ui->CaptainLine->setText(captain);
        ui->CVoteLine->setText(cVotes);
        ui->ViceCaptainLine->setText(vice);
        ui->VCVoteLine->setText(vcVotes);
        ui->TotalVoteCountLineEdit->setText(tvCount);
        ui->ValidVoteCountLineEdit->setText(vavCount);
    }

}

// Processes user's change of male spreadsheet filename
void MainWindow::on_FileName_textChanged()
{
    // Check if the directory specified in the file line edit is valid i.e it is non-empty and invalid
    if (ui->FileName->text() != "" && !QFile::exists(ui->FileName->text()))
    {
        // Output critical error message in case line edit text is invalid
        int ret = QMessageBox::critical(this, tr("GHS Voting: File Error"), tr("File directory specified does not exist!"), QMessageBox::Ok);

        // Check if the user has pressed the ok button
        if(ret == QMessageBox::Ok) //
            ui->FileName->clear(); // Clear line edit so a new file directory can be specified
    }
    // Checks if the directory specified in the file line edit is non-empty i.e it is passed the validity test and is non-empty so it can be passed to QFile
    else if (ui->FileName->text() != "") {
        // Set the file of voting data to the text in the file line edit
        votesFilePath = ui->FileName->text();
        filepathSet = true;
    }
    else if (ui->FileName->text() == "")
        filepathSet = false;
}

void MainWindow::on_SheetNameLineEdit_textChanged(const QString &arg1)
{
    // Get the sheet name for the Excel File
    sheetName = ui->SheetNameLineEdit->text();
    if (sheetName != "")
        sheetNameSet = true;
    else
        sheetNameSet = false;
}
