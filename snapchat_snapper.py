import sys
from PyQt6.QtCore import *
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QToolBar, QFileDialog
from PyQt6.QtGui import QAction
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        # Set window title and size
        self.setWindowTitle("Snapchat Web - Snapper V1.0")
        self.setGeometry(100, 100, 1280, 800)

        # Create a QWebEngineView widget (the browser)
        self.browser = QWebEngineView()

        # Accept all cookies to emulate real browser behavior
        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpUserAgent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Safari/537.36"
        )
        profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies)

        # Load Snapchat web URL
        self.browser.setUrl(QUrl("https://web.snapchat.com"))

        # Inject JavaScript to simulate interaction
        self.browser.page().loadFinished.connect(self.inject_javascript)

        # Set up a layout for the browser
        layout = QVBoxLayout()
        layout.addWidget(self.browser)

        # Container widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Add a toolbar to emulate browser navigation (Back, Forward, Reload)
        self.add_navigation_toolbar()

    def add_navigation_toolbar(self):
        # Create a toolbar
        toolbar = QToolBar(self)
        self.addToolBar(toolbar)

        # Back button
        back_action = QAction('Back', self)
        back_action.triggered.connect(self.browser.back)
        toolbar.addAction(back_action)

        # Forward button
        forward_action = QAction('Forward', self)
        forward_action.triggered.connect(self.browser.forward)
        toolbar.addAction(forward_action)

        # Reload button
        reload_action = QAction('Reload', self)
        reload_action.triggered.connect(self.browser.reload)
        toolbar.addAction(reload_action)

        # Stop loading button
        stop_action = QAction('Stop', self)
        stop_action.triggered.connect(self.browser.stop)
        toolbar.addAction(stop_action)

        # Screenshot button
        screenshot_action = QAction('Screenshot', self)
        screenshot_action.triggered.connect(self.schedule_screenshot)
        toolbar.addAction(screenshot_action)

    def inject_javascript(self):
        """Inject JavaScript to simulate user interactions and mask click events."""
        js_code = """
        // Simulate user scrolling to mimic natural behavior
        window.scrollBy(0, 500);  // Scroll down 500px

        // Override the native click function to mask click behavior
        HTMLElement.prototype.realClick = HTMLElement.prototype.click;
        HTMLElement.prototype.click = function() {
            var event = new MouseEvent('click', {
                bubbles: true,
                cancelable: true,
                view: window
            });
            this.dispatchEvent(event);
        };

        // Example: Click on a specific chat element (replace with the correct selector)
        let chatElement = document.querySelector('your-chat-element-selector');
        if (chatElement) {
            chatElement.click();
        }
        """
        # Inject JavaScript into the web page
        self.browser.page().runJavaScript(js_code)

    def schedule_screenshot(self):
        """Schedule the screenshot to be taken after a short delay."""
        self.screenshot_timer = QTimer()
        self.screenshot_timer.setSingleShot(True)  # Only run once
        self.screenshot_timer.timeout.connect(self.take_screenshot)
        self.screenshot_timer.start(1000)  # Adjust the delay (in milliseconds) as needed

    def take_screenshot(self):
        """Takes a screenshot of the current webpage."""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Screenshot", "", "PNG Files (*.png);;All Files (*)")
        if file_path:
            # Capture a screenshot of the web page directly using the QWebEngineView
            self.browser.grab().save(file_path, "PNG")

if __name__ == "__main__":
    # Initialize the Qt Application
    app = QApplication(sys.argv)
    window = MainWindow()

    # Show the window
    window.show()

    # Execute the application
    sys.exit(app.exec())
