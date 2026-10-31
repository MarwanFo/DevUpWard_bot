import React, { useRef, useState } from 'react';
import { UploadCloud, X, Image as ImageIcon, Loader2, Link2 } from 'lucide-react';
import ApiService from '../services/api';


interface ImageUploadProps {
  label: string;
  value?: string;
  onChange: (url: string) => void;
  folder?: string;
  aspectRatio?: 'square' | 'banner';
}

export const ImageUpload: React.FC<ImageUploadProps> = ({
  label,
  value,
  onChange,
  folder = 'avatars',
  aspectRatio = 'square',
}) => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const [showUrlInput, setShowUrlInput] = useState(false);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      setUploading(true);
      setError('');
      const res = await ApiService.uploadImage(file, folder);
      if (res.data.url) {
        onChange(res.data.url);
      }
    } catch (err: any) {
      console.error(err);
      setError(
        err?.response?.data?.detail ||
          'Upload failed. Make sure Cloudinary credentials are set in .env or Settings.'
      );
    } finally {
      setUploading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <label className="block text-xs font-medium text-slate-300">{label}</label>
        <button
          type="button"
          onClick={() => setShowUrlInput(!showUrlInput)}
          className="text-[11px] text-indigo-400 hover:text-indigo-300 flex items-center gap-1 transition-colors"
        >
          <Link2 className="w-3 h-3" />
          <span>{showUrlInput ? 'Hide URL input' : 'Paste direct URL'}</span>
        </button>
      </div>

      {error && (
        <div className="p-2.5 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs">
          {error}
        </div>
      )}

      {/* Main Upload Box */}
      <div className="flex items-start gap-4">
        {/* Preview Container */}
        {value ? (
          <div
            className={`relative rounded-2xl overflow-hidden border border-slate-700 bg-slate-950 shrink-0 shadow-md ${
              aspectRatio === 'square' ? 'w-20 h-20' : 'w-36 h-20'
            }`}
          >
            <img src={value} alt="Preview" className="w-full h-full object-cover" />
            <button
              type="button"
              onClick={() => onChange('')}
              className="absolute top-1 right-1 p-1 rounded-full bg-black/70 hover:bg-rose-600 text-white transition-colors"
              title="Remove image"
            >
              <X className="w-3 h-3" />
            </button>
          </div>
        ) : (
          <div
            className={`rounded-2xl border-2 border-dashed border-slate-800 bg-slate-950/60 flex flex-col items-center justify-center text-slate-600 shrink-0 ${
              aspectRatio === 'square' ? 'w-20 h-20' : 'w-36 h-20'
            }`}
          >
            <ImageIcon className="w-6 h-6" />
          </div>
        )}

        {/* Upload Action Area */}
        <div className="flex-1 space-y-2">
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            className="hidden"
          />

          <button
            type="button"
            disabled={uploading}
            onClick={() => fileInputRef.current?.click()}
            className="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xs font-semibold border border-slate-700 transition-colors disabled:opacity-50 shadow-sm"
          >
            {uploading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin text-indigo-400" />
                <span>Uploading to Cloudinary...</span>
              </>
            ) : (
              <>
                <UploadCloud className="w-4 h-4 text-indigo-400" />
                <span>{value ? 'Change Photo (Cloudinary)' : 'Upload Photo to Cloudinary'}</span>
              </>
            )}
          </button>

          <p className="text-[11px] text-slate-500">
            Supports JPG, PNG, WebP, GIF. Automatically optimized and hosted via Cloudinary CDN.
          </p>
        </div>
      </div>

      {/* Direct URL Fallback input */}
      {showUrlInput && (
        <div className="pt-2">
          <input
            type="url"
            value={value || ''}
            onChange={(e) => onChange(e.target.value)}
            placeholder="https://res.cloudinary.com/..."
            className="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-indigo-500"
          />
        </div>
      )}
    </div>
  );
};

export default ImageUpload;
