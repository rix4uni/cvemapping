/*
 * Copyright (C) 2019 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package com.android.providers.media.scan;

import static java.util.Objects.requireNonNull;

import android.annotation.NonNull;
import android.content.Context;
import android.net.Uri;
import android.os.Trace;
import android.provider.MediaStore;
import android.util.Log;

import libcore.net.MimeUtils;

import java.io.File;
import java.io.IOException;

public class LegacyMediaScanner implements MediaScanner {
    private static final String TAG = "LegacyMediaScanner";

    private final Context mContext;

    public LegacyMediaScanner(Context context) {
        mContext = context;
    }

    @Override
    public Context getContext() {
        return mContext;
    }

    @Override
    public void scanDirectory(File file) {
        requireNonNull(file);
        try {
            file = file.getCanonicalFile();
        } catch (IOException e) {
            Log.e(TAG, "Couldn't canonicalize directory to scan" + file, e);
            return;
        }

        final String path = file.getAbsolutePath();
        final String volumeName = MediaStore.getVolumeName(file);

        Trace.traceBegin(Trace.TRACE_TAG_DATABASE, "scanDirectory");
        try (android.media.MediaScanner scanner =
                new android.media.MediaScanner(mContext, volumeName)) {
            scanner.scanDirectories(new String[] { path });
        } finally {
            Trace.traceEnd(Trace.TRACE_TAG_DATABASE);
        }
    }

    @Override
    public Uri scanFile(@NonNull File file) {
        requireNonNull(file);
        try {
            file = file.getCanonicalFile();
        } catch (IOException e) {
            Log.e(TAG, "Couldn't canonicalize file to scan" + file, e);
            return null;
        }

        final String path = file.getAbsolutePath();
        final String volumeName = MediaStore.getVolumeName(file);

        Trace.traceBegin(Trace.TRACE_TAG_DATABASE, "scanFile");
        try (android.media.MediaScanner scanner =
                new android.media.MediaScanner(mContext, volumeName)) {
            final String ext = path.substring(path.lastIndexOf('.') + 1);
            return scanner.scanSingleFile(path,
                    MimeUtils.guessMimeTypeFromExtension(ext));
        } finally {
            Trace.traceEnd(Trace.TRACE_TAG_DATABASE);
        }
    }

    @Override
    public void onDetachVolume(String volumeName) {
        // Ignored
    }
}
