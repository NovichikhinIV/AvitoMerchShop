"use client";

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { AuthContext } from '../context/AuthContext';
import { useContext } from "react";

export default function PrivateRoute({ children }) {
    const router = useRouter();
    const { isAuthenticated } = useContext(AuthContext);

    useEffect(() => {
        if (!isAuthenticated) {
            router.push('/login'); 
        }
    }, [router, isAuthenticated]);

    return children;
}
