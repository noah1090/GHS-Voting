#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <string>
#include <fstream>
#include <vector>
#include <cstdio>
#include <cstdlib>

#include <QMainWindow>
#include <QFileDialog>
#include <QStandardPaths>
#include <QDebug>
#include <QFile>
#include <QMessageBox>
#include <QCloseEvent>
#include <QString>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private:
    Ui::MainWindow *ui;
    QFileDialog *fileDialog;

    QString writeFilePath = "vote_data_filepath.txt";
    QString resultsFilePath = "results.txt";
    QString votesFilePath = "";
    QString oldVoteFilePath;
    QString sheetName;
    bool sheetNameSet = false;
    bool filepathSet = false;

private slots:
    void on_OpenFileButton_clicked();

    void on_RunButton_clicked();

    void on_FileName_textChanged();

    void closeEvent(QCloseEvent *event);

    void on_SheetNameLineEdit_textChanged(const QString &arg1);
};

#endif // MAINWINDOW_H
