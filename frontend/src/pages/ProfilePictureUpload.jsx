import React, { useState, useContext } from 'react';
import { Button } from '../components';
import { useNavigate } from 'react-router-dom';
import { faUser } from '@fortawesome/free-solid-svg-icons';
import api from '../helpers/AxiosClient';
import AuthContext from '../helpers/AuthContext';

// VULN-F4G5H6: Path Traversal & VULN-I7J8K9: File Upload
const ProfilePictureUpload = () => {
    const navigate = useNavigate();
    const authCtx = useContext(AuthContext);
    const [filename, setFilename] = useState('');
    const [profileUrl, setProfileUrl] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setSuccess('');

        try {
            // VULN-F4G5H6: Filename not sanitized (path traversal)
            // VULN-I7J8K9: No file type validation
            const response = await api.post('/auth/profile-picture/upload/', {
                filename: filename,
                profile_url: profileUrl
            });
            
            setSuccess('Profile picture updated successfully!');
            
            // Update auth context with new profile pic
            if (authCtx.user) {
                authCtx.user.profilePic = response.profilePic;
            }
        } catch (err) {
            setError(err.response?.data?.error || 'Failed to upload profile picture');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className='flex gap-8 rounded-lg items-center w-full h-[calc(100vh-10rem)]'>
            <div className='flex flex-col rounded-lg p-8 shadow-lg border-2 h-full w-full bg-container justify-center items-center md:p-16'>
                <div className='text-4xl font-bold text-center'>
                    Upload Profile Picture
                </div>
                <hr className='my-6 border-2 rounded-lg w-1/2' />
                
                <form onSubmit={handleSubmit} className='w-full max-w-md space-y-4'>
                    <div>
                        <label htmlFor='filename' className='block text-sm font-medium mb-2'>
                            Filename (with path)
                        </label>
                        <input
                            type='text'
                            id='filename'
                            value={filename}
                            onChange={(e) => setFilename(e.target.value)}
                            required
                            className='w-full px-4 py-2 border-2 rounded-lg focus:outline-none focus:border-blue-500'
                            placeholder='e.g., ../../etc/passwd or profile.jpg'
                        />
                        <p className='text-xs text-gray-500 mt-1'>Try path traversal: ../../../test.jpg</p>
                    </div>
                    
                    <div>
                        <label htmlFor='profileUrl' className='block text-sm font-medium mb-2'>
                            Profile Picture URL
                        </label>
                        <input
                            type='text'
                            id='profileUrl'
                            value={profileUrl}
                            onChange={(e) => setProfileUrl(e.target.value)}
                            className='w-full px-4 py-2 border-2 rounded-lg focus:outline-none focus:border-blue-500'
                            placeholder='https://example.com/profile.jpg'
                        />
                    </div>
                    
                    {error && (
                        <div className='text-red-500 text-sm text-center'>
                            {error}
                        </div>
                    )}
                    
                    {success && (
                        <div className='text-green-500 text-sm text-center'>
                            {success}
                        </div>
                    )}
                    
                    <Button 
                        type="submit" 
                        className="py-2 w-full" 
                        isActive 
                        icon={faUser} 
                        text={loading ? "Uploading..." : "Upload"}
                        disabled={loading}
                    />
                </form>

                <div className='mt-4 text-center'>
                    <button 
                        onClick={() => navigate('/')} 
                        className='text-blue-500 font-bold underline'
                    >
                        Back to Home
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ProfilePictureUpload;
