"use client";

import { useState, useEffect } from "react";
import { getInfoAPI } from "../../utils/api";
import PrivateRoute from "../../components/PrivateRoute";
import { useRouter } from "next/navigation";
import { AuthContext } from '../../context/AuthContext';
import { useContext } from "react";
import styles from './page.module.css';

export default function Inventory() {
  const { isAuthenticated } = useContext(AuthContext);
  const [inventory, setInventory] = useState([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter(); 

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/login"); 
      return;
    }

    async function loadInventory() {
      try {
        const data = await getInfoAPI();
        setInventory(data.inventory.sort((a, b) => b.quantity - a.quantity));
      } catch (error) {
        console.error("Ошибка загрузки инвентаря:", error);
      } finally {
        setLoading(false);
      }
    }

    loadInventory();
  }, [router, isAuthenticated]);

  return (
    <PrivateRoute>
      <div className={styles.inventory}>
        <h1 className={styles.inventory__title}>Ваш инвентарь</h1>
        {loading ? (
          <p className={styles.inventory__loading}>Загрузка инвентаря...</p>
        ) : inventory.length === 0 ? (
          <p className={styles.inventory__empty}>У вас нет купленных товаров.</p>
        ) : (
          <div>
            {inventory.map((item, index) => (
              <div key={index} className={styles.inventory__item}>
                <h2 className={styles.inventory__item_name}>{item.type}</h2>
                <p className={styles.inventory__item_quantity}>Количество: {item.quantity}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </PrivateRoute>
  );
}
