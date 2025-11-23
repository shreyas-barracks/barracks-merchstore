import React from 'react';

const SearchFilter = ({ searchQuery, setSearchQuery, onSearch }) => {
    const handleSubmit = (e) => {
        e.preventDefault();
        onSearch();
    };

    const handleClear = () => {
        setSearchQuery('');
        onSearch('');
    };

    return (
        <form onSubmit={handleSubmit} className='flex gap-2 mb-4'>
            <div className='flex-1 relative'>
                <input
                    type='text'
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder='Search products by name or description...'
                    className='w-full px-4 py-2 border-2 rounded-lg focus:outline-none focus:border-blue-500'
                />
                {searchQuery && (
                    <button
                        type='button'
                        onClick={handleClear}
                        className='absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700'
                    >
                        ✕
                    </button>
                )}
            </div>
            <button
                type='submit'
                className='px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors'
            >
                Search
            </button>
        </form>
    );
};

export default SearchFilter;
