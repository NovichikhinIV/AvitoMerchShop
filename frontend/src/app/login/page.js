"use client";

import { useState, useContext, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { AuthContext } from '../../context/AuthContext';
import styles from './page.module.css';

export default function LoginPage() {
    const { isAuthenticated, login } = useContext(AuthContext);
    const router = useRouter();

    useEffect(() => {
        if (isAuthenticated) {
            router.push('/');
        }
    }, [isAuthenticated, router]);

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(''); 

        if (!username.trim() || !password.trim()) {
            setError('Заполните все поля');
            return;
        }

        try {
            const success = await login(username, password);
            if (success) {
                router.push('/');
            } else {
                setError('Неверные данные для входа');
            }
        } catch (err) {
            setError('Ошибка сервера. Попробуйте позже.');
        }
    };

    return (
        <div className={styles.login}>
            <div className={styles.login__container}>
                <h1 className={styles.login__title}>Войти</h1>
                <form onSubmit={handleSubmit} className={styles.login__form}>
                    <div>
                        <label htmlFor="username" className={styles.login__label}>Имя пользователя</label>
                        <input
                            type="text"
                            id="username"
                            className={styles.login__input}
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                        />
                    </div>
                    <div>
                        <label htmlFor="password" className={styles.login__label}>Пароль</label>
                        <input
                            type="password"
                            id="password"
                            className={styles.login__input}
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </div>
                    <button type="submit" className={styles.login__button}>Войти</button>
                    {error && <p className={styles.login__error}>{error}</p>}
                </form>
            </div>
        </div>
    );
}
