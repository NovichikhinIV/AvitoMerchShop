"use client";

// pages/shop.js
import { useState, useEffect } from "react";
import { getProductsAPI, buyItemAPI } from "../utils/api";
import { AuthContext } from '../context/AuthContext';
import { useContext } from "react";
import styles from './page.module.css';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

export default function Shop() {
  const { isAuthenticated } = useContext(AuthContext);
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadProducts() {
      try {
        const data = await getProductsAPI();
        setProducts(data);
      } catch (error) {
        console.error("Ошибка загрузки товаров:", error);
      } finally {
        setLoading(false);
      }
    }

    loadProducts();
  }, [isAuthenticated]);

  const handleBuy = async (productId) => {
    try {
      await buyItemAPI(productId);
      toast.success("Покупка успешна!"); 
    } catch (error) {
      if (error.message.includes("400")) {
        toast.error("Ошибка: недостаточно монет для покупки.");
      } else {
        toast.error(`Ошибка: ${error.message}`);
      }
    }
  };

  return (
    <div className={styles.shop}>
      <h1 className={styles.shop__title}>Магазин</h1>
      {loading ? (
        <p className={styles.shop__loading}>Загрузка товаров...</p>
      ) : products.length === 0 ? (
        <p className={styles.shop__loading}>Нет доступных товаров.</p>
      ) : (
        <div className={styles.shop__product_list}>
          {products.map((product) => (
            <div key={product.id} className={styles.shop__product_item}>
              <h2 className={styles.shop__product_name}>{product.name}</h2>
              <p className={styles.shop__product_price}>{product.price} Рублей</p>
              {isAuthenticated && (
                <button className={styles.shop__buy_button} onClick={() => handleBuy(product.id)}>Купить</button>
              )}
            </div>
          ))}
        </div>
      )}
      <ToastContainer />
    </div>
  );
}
