import React from 'react';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { 
    faBug, 
    faUsers, 
    faKey, 
    faTrash, 
    faImage, 
    faFlask 
} from '@fortawesome/free-solid-svg-icons';

const VulnTab = () => {
    const vulnLinks = [
        { 
            path: '/vuln-testing', 
            icon: faFlask, 
            name: 'Test All Vulns',
            color: 'text-red-600',
            desc: 'Test all 30 vulnerabilities'
        },
        { 
            path: '/users', 
            icon: faUsers, 
            name: 'User List',
            color: 'text-blue-600',
            desc: 'VULN-Q7R8S9: View all users'
        },
        { 
            path: '/forgot-password', 
            icon: faKey, 
            name: 'Reset Password',
            color: 'text-orange-600',
            desc: 'VULN-L1M2N3: No verification'
        },
        { 
            path: '/delete-account', 
            icon: faTrash, 
            name: 'Delete Account',
            color: 'text-red-600',
            desc: 'VULN-M4N5O6: Clickjacking'
        },
        { 
            path: '/profile-picture', 
            icon: faImage, 
            name: 'Upload Picture',
            color: 'text-green-600',
            desc: 'VULN-F4G5H6: Path traversal'
        },
    ];

    return (
        <div className='h-full flex flex-col space-y-4 overflow-y-auto'>
            <div className='bg-yellow-50 border-2 border-yellow-400 rounded-lg p-4'>
                <div className='flex items-center gap-2 mb-2'>
                    <FontAwesomeIcon icon={faBug} className='text-yellow-600' />
                    <h3 className='font-bold text-lg'>Vulnerability Testing</h3>
                </div>
                <p className='text-sm text-gray-700'>
                    This application has 30 intentional security vulnerabilities for bug bounty testing.
                </p>
            </div>

            <div className='grid grid-cols-1 gap-3'>
                {vulnLinks.map((link, index) => (
                    <Link
                        key={index}
                        to={link.path}
                        className='border-2 rounded-lg p-4 hover:shadow-lg hover:scale-105 transition-all bg-white'
                    >
                        <div className='flex items-start gap-3'>
                            <FontAwesomeIcon 
                                icon={link.icon} 
                                className={`${link.color} text-xl mt-1`} 
                            />
                            <div>
                                <div className='font-bold text-lg'>{link.name}</div>
                                <div className='text-sm text-gray-600'>{link.desc}</div>
                            </div>
                        </div>
                    </Link>
                ))}
            </div>

            <div className='bg-red-50 border-2 border-red-400 rounded-lg p-4 text-sm'>
                <p className='font-semibold mb-1'>⚠️ Security Notice:</p>
                <p className='text-gray-700'>
                    This is a deliberately vulnerable application for educational purposes. 
                    Do not use in production!
                </p>
            </div>
        </div>
    );
};

export default VulnTab;
