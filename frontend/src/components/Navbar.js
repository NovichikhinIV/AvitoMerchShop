// app/components/Navbar.js
"use client"; 

import Link from 'next/link'; 
import { useState, useEffect, useContext } from 'react';
import { useRouter } from 'next/navigation';
import { AuthContext } from '../context/AuthContext'; 
import styles from './Navbar.module.css';

export default function Navbar() {
    const { isAuthenticated, logout, user } = useContext(AuthContext);
    const router = useRouter();

    const handleLogout = () => {
        logout(); 
    };

    return (
        <nav className={styles.navbar}>
            <ul className={styles.navbar__list}>
                <li className={styles.navbar__item}><Link href="/" className={styles.navbar__link}>Магазин</Link></li>
                <li className={styles.navbar__item}><Link href="/inventory" className={styles.navbar__link}>Инвентарь</Link></li>
                <li className={styles.navbar__item}><Link href="/wallet" className={styles.navbar__link}>Кошелек</Link></li>
            </ul>
            <div className={styles.navbar__item}>
                {isAuthenticated ? ( 
                    <>
                        <span className={styles.username}>{user}</span>
                        <Link href="/" className={styles.navbar__link} onClick={handleLogout}>Выйти</Link>
                    </>
                ) : (
                    <Link href="/login" className={styles.navbar__link}>Войти</Link>
                )}
            </div>
        </nav>
    );
}
