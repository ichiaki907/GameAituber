import cv2
import time
import os

# ビデオソースの選択
video_source = 0  # または 'path/to/video.mp4'

# ビデオキャプチャオブジェクトの作成
cap = cv2.VideoCapture(video_source)

# 保存先フォルダの確認と作成
save_folder = "frame"
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# フレームインデックス
frame_index = 0

# 最大の保存画像数
max_frames = 5

# 最初のフレームのタイムスタンプを取得
start_time = time.time()

# ユーザーが 'q' を押すまでループ
while True:
    # 経過時間をチェック
    elapsed_time = time.time() - start_time

    # フレームを読み込む
    ret, frame = cap.read()
    
    # フレームが正しく読み込まれたか確認
    if not ret:
        break

    # 経過時間が1秒以上のときに画像を保存
    if elapsed_time > frame_index:
        # 画像を保存
        filename = f'saved_frame_{frame_index % max_frames}.jpg'
        cv2.imwrite(os.path.join(save_folder, filename), frame)
        
        # 保存した画像のインデックスを更新
        frame_index += 1
        
        # 保存画像数が最大数を超えたら、最も古い画像を削除
        if frame_index >= max_frames:
            oldest_frame_index = frame_index - max_frames
            oldest_filename = f'saved_frame_{oldest_frame_index % max_frames}.jpg'
            oldest_filepath = os.path.join(save_folder, oldest_filename)
            if os.path.exists(oldest_filepath):
                os.remove(oldest_filepath)
        
        print(f'Saved frame {frame_index}')
        
    # 'q'キーを押すとループから抜ける
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# キャプチャのリリース
cap.release()
cv2.destroyAllWindows()