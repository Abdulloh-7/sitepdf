const btn = document.getElementById('open-btn');
const pinInput = document.getElementById('pin');
const notification = document.getElementById('notification');
const captchaContainer = document.getElementById('captcha-container');
const captchaInput = document.getElementById('captcha');

btn.addEventListener('click', async () => {
  const pin = pinInput.value;
  const captcha = captchaInput ? captchaInput.value : '';
  const urlParams = new URLSearchParams(window.location.search);
  const guid = urlParams.get('guid') || 'abcd-1234'; // по умолчанию

  const formData = new FormData();
  formData.append('pin', pin);
  if (captcha) formData.append('captcha', captcha);

  try {
    const response = await fetch(`/file?guid=${guid}`, {
      method: 'POST',
      body: formData
    });

    if (response.ok) {
      const blob = await response.blob();
      const fileUrl = URL.createObjectURL(blob);
      window.open(fileUrl, '_blank');
      notification.style.display = 'none';
    } else {
      const data = await response.json();
      notification.textContent = data.error;
      notification.style.display = 'block';

      if (data.attempts >= 4) {
        captchaContainer.style.display = 'block';
      }
    }
  } catch (err) {
    notification.textContent = "Ошибка сервера!";
    notification.style.display = 'block';
  }
});