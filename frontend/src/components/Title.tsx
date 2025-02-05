import { useState } from 'react';
import axios from 'axios';

type Props = {
  setMessages: any;
};

function Title({ setMessages }: Props) {
  const [isResetting, setIsResetting] = useState(false);

  // Reset the conversation
  const resetConversation = async () => {
    setIsResetting(true);

    await axios.get('http://localhost:8000/reset').then((res) => {
      if (res.status == 200) {
        setMessages([]);
      } else {
        console.error('Error with the API request');
      }
    }).catch((err) => {
      console.error(err);
    });
    setIsResetting(false);
  };

  return (
    <div>
      <button onClick={resetConversation} className='bg-sky-500 p-3'>RESET</button>
    </div>
  )
}

export default Title