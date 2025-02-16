// app/layout.js
"use client";

import Navbar from '../components/Navbar'; 
import { AuthProvider } from "../context/AuthContext";
import styles from './globals.css'; 

export default function Layout({ children }) {
    return (
        <AuthProvider>
            <html lang="ru">
                <head>
                    <meta charSet="UTF-8" />
                    <meta name="viewport" content="width=device-width, initial-scale=1" />
                    <title>Avito Shop</title>
                    <link rel="icon" type="image/png" href="favicon.png" />
                </head>
                <body className={styles.layout}>
                    <Navbar />
                    <main className={styles.layout__main}>{children}</main>
                </body>
            </html>
        </AuthProvider>
    );
}
