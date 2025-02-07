Title: JAVA Application
Date: 2025-02-07
Category: Backend
Tags: Java
Author: Yoga

### Memory Leak Monitoring

Java is not really efficient in its garbage collection so we need to be mindful of potential memory leaks. Here we list two ways to help identify and alert us to potential memory issues.

1. **Code Analysis with VisualVM:**

    VisualVM is a powerful tool that comes with the Java Development Kit (JDK). It provides a visual interface for monitoring Java applications while they are running, and it can also be used for profiling and diagnosing memory issues.

2. **Monitoring with Azure Alerts after golive:**

    Azure Alerts can be configured to monitor various metrics related to our application's performance, including memory usage. By setting up alerts based on memory metrics, we can be notified when memory usage exceeds a certain threshold, which could indicate a potential memory leak or other performance issues.