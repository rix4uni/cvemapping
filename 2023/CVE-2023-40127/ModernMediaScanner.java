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

import static android.media.MediaMetadataRetriever.METADATA_KEY_ALBUM;
import static android.media.MediaMetadataRetriever.METADATA_KEY_ALBUMARTIST;
import static android.media.MediaMetadataRetriever.METADATA_KEY_ARTIST;
import static android.media.MediaMetadataRetriever.METADATA_KEY_CD_TRACK_NUMBER;
import static android.media.MediaMetadataRetriever.METADATA_KEY_COLOR_RANGE;
import static android.media.MediaMetadataRetriever.METADATA_KEY_COLOR_STANDARD;
import static android.media.MediaMetadataRetriever.METADATA_KEY_COLOR_TRANSFER;
import static android.media.MediaMetadataRetriever.METADATA_KEY_COMPILATION;
import static android.media.MediaMetadataRetriever.METADATA_KEY_COMPOSER;
import static android.media.MediaMetadataRetriever.METADATA_KEY_DATE;
import static android.media.MediaMetadataRetriever.METADATA_KEY_DURATION;
import static android.media.MediaMetadataRetriever.METADATA_KEY_GENRE;
import static android.media.MediaMetadataRetriever.METADATA_KEY_IS_DRM;
import static android.media.MediaMetadataRetriever.METADATA_KEY_TITLE;
import static android.media.MediaMetadataRetriever.METADATA_KEY_VIDEO_HEIGHT;
import static android.media.MediaMetadataRetriever.METADATA_KEY_VIDEO_WIDTH;
import static android.media.MediaMetadataRetriever.METADATA_KEY_YEAR;
import static android.os.Trace.TRACE_TAG_DATABASE;
import static android.provider.MediaStore.AUTHORITY;
import static android.provider.MediaStore.UNKNOWN_STRING;
import static android.text.format.DateUtils.HOUR_IN_MILLIS;
import static android.text.format.DateUtils.MINUTE_IN_MILLIS;

import static java.util.Objects.requireNonNull;

import android.annotation.CurrentTimeMillisLong;
import android.annotation.CurrentTimeSecondsLong;
import android.annotation.NonNull;
import android.annotation.Nullable;
import android.content.ContentProviderClient;
import android.content.ContentProviderOperation;
import android.content.ContentProviderResult;
import android.content.ContentResolver;
import android.content.ContentUris;
import android.content.Context;
import android.content.OperationApplicationException;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.media.ExifInterface;
import android.media.MediaFile;
import android.media.MediaMetadataRetriever;
import android.mtp.MtpConstants;
import android.net.Uri;
import android.os.Build;
import android.os.CancellationSignal;
import android.os.Environment;
import android.os.FileUtils;
import android.os.OperationCanceledException;
import android.os.RemoteException;
import android.os.Trace;
import android.provider.MediaStore;
import android.provider.MediaStore.Audio.AudioColumns;
import android.provider.MediaStore.Audio.PlaylistsColumns;
import android.provider.MediaStore.Files.FileColumns;
import android.provider.MediaStore.Images.ImageColumns;
import android.provider.MediaStore.MediaColumns;
import android.provider.MediaStore.Video.VideoColumns;
import android.text.TextUtils;
import android.util.ArrayMap;
import android.util.Log;
import android.util.LongArray;

import com.android.internal.annotations.GuardedBy;
import com.android.internal.annotations.VisibleForTesting;
import com.android.providers.media.util.IsoInterface;
import com.android.providers.media.util.XmpInterface;

import libcore.net.MimeUtils;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.file.FileVisitResult;
import java.nio.file.FileVisitor;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.attribute.BasicFileAttributes;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Locale;
import java.util.Optional;
import java.util.TimeZone;
import java.util.regex.Pattern;

/**
 * Modern implementation of media scanner.
 * <p>
 * This is a bug-compatible reimplementation of the legacy media scanner, but
 * written purely in managed code for better testability and long-term
 * maintainability.
 * <p>
 * Initial tests shows it performing roughly on-par with the legacy scanner.
 * <p>
 * In general, we start by populating metadata based on file attributes, and
 * then overwrite with any valid metadata found using
 * {@link MediaMetadataRetriever}, {@link ExifInterface}, and
 * {@link XmpInterface}, each with increasing levels of trust.
 */
public class ModernMediaScanner implements MediaScanner {
    private static final String TAG = "ModernMediaScanner";
    private static final boolean LOGW = Log.isLoggable(TAG, Log.WARN);
    private static final boolean LOGD = Log.isLoggable(TAG, Log.DEBUG);
    private static final boolean LOGV = Log.isLoggable(TAG, Log.VERBOSE);

    // TODO: add DRM support

    // TODO: refactor to use UPSERT once we have SQLite 3.24.0

    // TODO: deprecate playlist editing
    // TODO: deprecate PARENT column, since callers can't see directories

    private static final SimpleDateFormat sDateFormat;

    static {
        sDateFormat = new SimpleDateFormat("yyyyMMdd'T'HHmmss");
        sDateFormat.setTimeZone(TimeZone.getTimeZone("UTC"));
    }

    private static final int BATCH_SIZE = 32;

    private static final Pattern PATTERN_VISIBLE = Pattern.compile(
            "(?i)^/storage/[^/]+(?:/[0-9]+)?(?:/Android/sandbox/([^/]+))?$");
    private static final Pattern PATTERN_INVISIBLE = Pattern.compile(
            "(?i)^/storage/[^/]+(?:/[0-9]+)?(?:/Android/sandbox/([^/]+))?/Android/(?:data|obb)$");

    private final Context mContext;

    /**
     * Map from volume name to signals that can be used to cancel any active
     * scan operations on those volumes.
     */
    @GuardedBy("mSignals")
    private final ArrayMap<String, CancellationSignal> mSignals = new ArrayMap<>();

    public ModernMediaScanner(Context context) {
        mContext = context;
    }

    @Override
    public Context getContext() {
        return mContext;
    }

    @Override
    public void scanDirectory(@NonNull File file) {
        requireNonNull(file);
        try {
            file = file.getCanonicalFile();
        } catch (IOException e) {
            Log.e(TAG, "Couldn't canonicalize directory to scan" + file, e);
            return;
        }

        try (Scan scan = new Scan(file)) {
            scan.run();
        } catch (OperationCanceledException ignored) {
        }
    }

    @Override
    @Nullable
    public Uri scanFile(@NonNull File file) {
        requireNonNull(file);
        try {
            file = file.getCanonicalFile();
        } catch (IOException e) {
            Log.e(TAG, "Couldn't canonicalize file to scan" + file, e);
            return null;
        }

        try (Scan scan = new Scan(file)) {
            scan.run();
            return scan.mFirstResult;
        } catch (OperationCanceledException ignored) {
            return null;
        }
    }

    @Override
    public void onDetachVolume(String volumeName) {
        synchronized (mSignals) {
            final CancellationSignal signal = mSignals.remove(volumeName);
            if (signal != null) {
                signal.cancel();
            }
        }
    }

    private CancellationSignal getOrCreateSignal(String volumeName) {
        synchronized (mSignals) {
            CancellationSignal signal = mSignals.get(volumeName);
            if (signal == null) {
                signal = new CancellationSignal();
                mSignals.put(volumeName, signal);
            }
            return signal;
        }
    }

    /**
     * Individual scan request for a specific file or directory. When run it
     * will traverse all included media files under the requested location,
     * reconciling them against {@link MediaStore}.
     */
    private class Scan implements Runnable, FileVisitor<Path>, AutoCloseable {
        private final ContentProviderClient mClient;
        private final ContentResolver mResolver;

        private final File mRoot;
        private final String mVolumeName;
        private final Uri mFilesUri;
        private final CancellationSignal mSignal;

        private final boolean mSingleFile;
        private final ArrayList<ContentProviderOperation> mPending = new ArrayList<>();
        private LongArray mScannedIds = new LongArray();
        private LongArray mUnknownIds = new LongArray();
        private LongArray mPlaylistIds = new LongArray();

        private Uri mFirstResult;

        public Scan(File root) {
            Trace.traceBegin(TRACE_TAG_DATABASE, "ctor");

            mClient = mContext.getContentResolver()
                    .acquireContentProviderClient(MediaStore.AUTHORITY);
            mResolver = ContentResolver.wrap(mClient.getLocalContentProvider());

            mRoot = root;
            mVolumeName = MediaStore.getVolumeName(root);
            mFilesUri = MediaStore.setIncludePending(MediaStore.Files.getContentUri(mVolumeName));
            mSignal = getOrCreateSignal(mVolumeName);

            mSingleFile = mRoot.isFile();

            Trace.traceEnd(TRACE_TAG_DATABASE);
        }

        @Override
        public void run() {
            // First, scan everything that should be visible under requested
            // location, tracking scanned IDs along the way
            walkFileTree();

            // Second, reconcile all items known in the database against all the
            // items we scanned above
            if (mSingleFile && mScannedIds.size() == 1) {
                // We can safely skip this step if the scan targeted a single
                // file which we scanned above
            } else {
                reconcileAndClean();
            }

            // Third, resolve any playlists that we scanned
            if (mPlaylistIds.size() > 0) {
                resolvePlaylists();
            }
        }

        private void walkFileTree() {
            mSignal.throwIfCanceled();
            if (!isDirectoryHiddenRecursive(mSingleFile ? mRoot.getParentFile() : mRoot)) {
                Trace.traceBegin(Trace.TRACE_TAG_DATABASE, "walkFileTree");
                try {
                    Files.walkFileTree(mRoot.toPath(), this);
                } catch (IOException e) {
                    // This should never happen, so yell loudly
                    throw new IllegalStateException(e);
                } finally {
                    Trace.traceEnd(Trace.TRACE_TAG_DATABASE);
                }
                applyPending();
            }
        }

        private void reconcileAndClean() {
            final long[] scannedIds = mScannedIds.toArray();
            Arrays.sort(scannedIds);

            // The query phase is split from the delete phase so that our query
            // remains stable if we need to paginate across multiple windows.
            mSignal.throwIfCanceled();
            Trace.traceBegin(Trace.TRACE_TAG_DATABASE, "reconcile");
            try (Cursor c = mResolver.query(mFilesUri,
                    new String[]{FileColumns._ID},
                    FileColumns.FORMAT + "!=? AND " + FileColumns.DATA + " LIKE ? ESCAPE '\\'",
                    new String[]{
                            // Ignore abstract playlists which don't have files on disk
                            String.valueOf(MtpConstants.FORMAT_ABSTRACT_AV_PLAYLIST),
                            escapeForLike(mRoot.getAbsolutePath()) + '%'
                    },
                    FileColumns._ID + " DESC", mSignal)) {
                while (c.moveToNext()) {
                    final long id = c.getLong(0);
                    if (Arrays.binarySearch(scannedIds, id) < 0) {
                        mUnknownIds.add(id);
                    }
                }
            } finally {
                Trace.traceEnd(Trace.TRACE_TAG_DATABASE);
            }

            // Third, clean all the unknown database entries found above
            mSignal.throwIfCanceled();
            Trace.traceBegin(Trace.TRACE_TAG_DATABASE, "clean");
            try {
                for (int i = 0; i < mUnknownIds.size(); i++) {
                    final long id = mUnknownIds.get(i);
                    if (LOGV) Log.v(TAG, "Cleaning " + id);
                    final Uri uri = MediaStore.Files.getContentUri(mVolumeName, id).buildUpon()
                            .appendQueryParameter(MediaStore.PARAM_DELETE_DATA, "false")
                            .build();
                    mPending.add(ContentProviderOperation.newDelete(uri).build());
                    maybeApplyPending();
                }
                applyPending();
            } finally {
                Trace.traceEnd(Trace.TRACE_TAG_DATABASE);
            }
        }

        private void resolvePlaylists() {
            mSignal.throwIfCanceled();
            for (int i = 0; i < mPlaylistIds.size(); i++) {
                final Uri uri = MediaStore.Files.getContentUri(mVolumeName, mPlaylistIds.get(i));
                try {
                    mPending.addAll(
                            PlaylistResolver.resolvePlaylist(mResolver, uri));
                    maybeApplyPending();
                } catch (IOException e) {
                    if (LOGW) Log.w(TAG, "Ignoring troubled playlist: " + uri, e);
                }
                applyPending();
            }
        }

        @Override
        public void close() {
            // Sanity check that we drained any pending operations
            if (!mPending.isEmpty()) {
                throw new IllegalStateException();
            }

            mClient.close();
        }

        @Override
        public FileVisitResult preVisitDirectory(Path dir, BasicFileAttributes attrs)
                throws IOException {
            // Possibly bail before digging into each directory
            mSignal.throwIfCanceled();

            if (isDirectoryHidden(dir.toFile())) {
                return FileVisitResult.SKIP_SUBTREE;
            }

            // Scan this directory as a normal file so that "parent" database
            // entries are created
            return visitFile(dir, attrs);
        }

        @Override
        public FileVisitResult visitFile(Path file, BasicFileAttributes attrs)
                throws IOException {
            if (LOGV) Log.v(TAG, "Visiting " + file);

            // Skip files that have already been scanned, and which haven't
            // changed since they were last scanned
            final File realFile = file.toFile();
            long existingId = -1;
            Trace.traceBegin(Trace.TRACE_TAG_DATABASE, "checkChanged");
            try (Cursor c = mResolver.query(mFilesUri,
                    new String[] { FileColumns._ID, FileColumns.DATE_MODIFIED, FileColumns.SIZE },
                    FileColumns.DATA + "=?", new String[] { realFile.getAbsolutePath() }, null)) {
                if (c.moveToFirst()) {
                    existingId = c.getLong(0);
                    final long dateModified = c.getLong(1);
                    final long size = c.getLong(2);

                    // Remember visiting this existing item, even if we skipped
                    // due to it being unchanged; this is needed so we don't
                    // delete the item during a later cleaning phase
                    mScannedIds.add(existingId);

                    // We also technically found our first result
                    if (mFirstResult == null) {
                        mFirstResult = MediaStore.Files.getContentUri(mVolumeName, existingId);
                    }

                    final boolean sameTime = (lastModifiedTime(realFile, attrs) == dateModified);
                    final boolean sameSize = (attrs.size() == size);
                    if (attrs.isDirectory() || (sameTime && sameSize)) {
                        if (LOGV) Log.v(TAG, "Skipping unchanged " + file);
                        return FileVisitResult.CONTINUE;
                    }
                }
            } finally {
                Trace.traceEnd(Trace.TRACE_TAG_DATABASE);
            }

            final ContentProviderOperation op;
            Trace.traceBegin(Trace.TRACE_TAG_DATABASE, "scanItem");
            try {
                op = scanItem(existingId, file.toFile(), attrs, mVolumeName);
            } finally {
                Trace.traceEnd(Trace.TRACE_TAG_DATABASE);
            }
            if (op != null) {
                mPending.add(op);
                maybeApplyPending();
            }
            return FileVisitResult.CONTINUE;
        }

        @Override
        public FileVisitResult visitFileFailed(Path file, IOException exc)
                throws IOException {
            Log.w(TAG, "Failed to visit " + file + ": " + exc);
            return FileVisitResult.CONTINUE;
        }

        @Override
        public FileVisitResult postVisitDirectory(Path dir, IOException exc)
                throws IOException {
            return FileVisitResult.CONTINUE;
        }

        private void maybeApplyPending() {
            if (mPending.size() > BATCH_SIZE) {
                applyPending();
            }
        }

        private void applyPending() {
            Trace.traceBegin(Trace.TRACE_TAG_DATABASE, "applyPending");
            try {
                ContentProviderResult[] results = mResolver.applyBatch(AUTHORITY, mPending);
                for (int index = 0; index < results.length; index++) {
                    ContentProviderResult result = results[index];
                    ContentProviderOperation operation = mPending.get(index);

                    Uri uri = result.uri;
                    if (uri != null) {
                        if (mFirstResult == null) {
                            mFirstResult = uri;
                        }
                        final long id = ContentUris.parseId(uri);
                        mScannedIds.add(id);
                    }

                    // Some operations don't return a URI, so check the original if necessary
                    Uri uriToCheck = uri == null ? operation.getUri() : uri;
                    if (uriToCheck != null) {
                        if (isPlaylist(uriToCheck)) {
                            // If this was a playlist, remember it so we can resolve
                            // its contents once all other media has been scanned
                            mPlaylistIds.add(ContentUris.parseId(uriToCheck));
                        }
                    }
                }
            } catch (RemoteException | OperationApplicationException e) {
                Log.w(TAG, "Failed to apply: " + e);
            } finally {
                mPending.clear();
                Trace.traceEnd(Trace.TRACE_TAG_DATABASE);
            }
        }
    }

    /**
     * Scan the requested file, returning a {@link ContentProviderOperation}
     * containing all indexed metadata, suitable for passing to a
     * {@link SQLiteDatabase#replace} operation.
     */
    private static @Nullable ContentProviderOperation scanItem(long existingId, File file,
            BasicFileAttributes attrs, String volumeName) {
        final String name = file.getName();
        if (name.startsWith(".")) {
            if (LOGD) Log.d(TAG, "Ignoring hidden file: " + file);
            return null;
        }

        try {
            final String mimeType;
            if (attrs.isDirectory()) {
                mimeType = null;
            } else {
                mimeType = MediaFile.getMimeTypeForFile(file.getPath());
            }

            if (attrs.isDirectory()) {
                return scanItemDirectory(existingId, file, attrs, mimeType, volumeName);
            } else if (MediaFile.isPlayListMimeType(mimeType)) {
                return scanItemPlaylist(existingId, file, attrs, mimeType, volumeName);
            } else if (MediaFile.isAudioMimeType(mimeType)) {
                return scanItemAudio(existingId, file, attrs, mimeType, volumeName);
            } else if (MediaFile.isVideoMimeType(mimeType)) {
                return scanItemVideo(existingId, file, attrs, mimeType, volumeName);
            } else if (MediaFile.isImageMimeType(mimeType)) {
                return scanItemImage(existingId, file, attrs, mimeType, volumeName);
            } else {
                return scanItemFile(existingId, file, attrs, mimeType, volumeName);
            }
        } catch (IOException e) {
            if (LOGW) Log.w(TAG, "Ignoring troubled file: " + file, e);
            return null;
        }
    }

    /**
     * Populate the given {@link ContentProviderOperation} with the generic
     * {@link MediaColumns} values that can be determined directly from the file
     * or its attributes.
     */
    private static void withGenericValues(ContentProviderOperation.Builder op,
            File file, BasicFileAttributes attrs, String mimeType) {
        op.withValue(MediaColumns.DATA, file.getAbsolutePath());
        op.withValue(MediaColumns.SIZE, attrs.size());
        op.withValue(MediaColumns.TITLE, extractName(file));
        op.withValue(MediaColumns.DATE_MODIFIED, lastModifiedTime(file, attrs));
        op.withValue(MediaColumns.DATE_TAKEN, null);
        op.withValue(MediaColumns.MIME_TYPE, mimeType);
        op.withValue(MediaColumns.IS_DRM, 0);
        op.withValue(MediaColumns.WIDTH, null);
        op.withValue(MediaColumns.HEIGHT, null);
        op.withValue(MediaColumns.DOCUMENT_ID, null);
        op.withValue(MediaColumns.INSTANCE_ID, null);
        op.withValue(MediaColumns.ORIGINAL_DOCUMENT_ID, null);
        op.withValue(MediaColumns.DURATION, null);
        op.withValue(MediaColumns.ORIENTATION, null);
    }

    /**
     * Populate the given {@link ContentProviderOperation} with the generic
     * {@link MediaColumns} values using the given XMP metadata.
     */
    private static void withXmpValues(ContentProviderOperation.Builder op,
            XmpInterface xmp, String mimeType) {
        op.withValue(MediaColumns.MIME_TYPE,
                maybeOverrideMimeType(mimeType, xmp.getFormat()));
        op.withValue(MediaColumns.DOCUMENT_ID, xmp.getDocumentId());
        op.withValue(MediaColumns.INSTANCE_ID, xmp.getInstanceId());
        op.withValue(MediaColumns.ORIGINAL_DOCUMENT_ID, xmp.getOriginalDocumentId());
    }

    /**
     * Overwrite a value in the given {@link ContentProviderOperation}, but only
     * when the given {@link Optional} value is present.
     */
    private static void withOptionalValue(ContentProviderOperation.Builder op,
            String key, Optional<?> value) {
        if (value.isPresent()) {
            op.withValue(key, value.get());
        }
    }

    private static @NonNull ContentProviderOperation scanItemDirectory(long existingId, File file,
            BasicFileAttributes attrs, String mimeType, String volumeName) throws IOException {
        final ContentProviderOperation.Builder op = newUpsert(
                MediaStore.Files.getContentUri(volumeName), existingId);
        try {
            withGenericValues(op, file, attrs, mimeType);
            op.withValue(FileColumns.MEDIA_TYPE, 0);
            op.withValue(FileColumns.FORMAT, MtpConstants.FORMAT_ASSOCIATION);
            op.withValue(FileColumns.MIME_TYPE, null);
        } catch (Exception e) {
            throw new IOException(e);
        }
        return op.build();
    }

    private static ArrayMap<String, String> sAudioTypes = new ArrayMap<>();

    static {
        sAudioTypes.put(Environment.DIRECTORY_RINGTONES, AudioColumns.IS_RINGTONE);
        sAudioTypes.put(Environment.DIRECTORY_NOTIFICATIONS, AudioColumns.IS_NOTIFICATION);
        sAudioTypes.put(Environment.DIRECTORY_ALARMS, AudioColumns.IS_ALARM);
        sAudioTypes.put(Environment.DIRECTORY_PODCASTS, AudioColumns.IS_PODCAST);
        sAudioTypes.put(Environment.DIRECTORY_AUDIOBOOKS, AudioColumns.IS_AUDIOBOOK);
        sAudioTypes.put(Environment.DIRECTORY_MUSIC, AudioColumns.IS_MUSIC);
    }

    private static @NonNull ContentProviderOperation scanItemAudio(long existingId, File file,
            BasicFileAttributes attrs, String mimeType, String volumeName) throws IOException {
        final ContentProviderOperation.Builder op = newUpsert(
                MediaStore.Audio.Media.getContentUri(volumeName), existingId);

        withGenericValues(op, file, attrs, mimeType);
        op.withValue(AudioColumns.ARTIST, UNKNOWN_STRING);
        op.withValue(AudioColumns.ALBUM_ARTIST, null);
        op.withValue(AudioColumns.COMPILATION, null);
        op.withValue(AudioColumns.COMPOSER, null);
        op.withValue(AudioColumns.ALBUM, file.getParentFile().getName());
        op.withValue(AudioColumns.TRACK, null);
        op.withValue(AudioColumns.YEAR, null);
        op.withValue(AudioColumns.GENRE, null);

        final String lowPath = file.getAbsolutePath().toLowerCase(Locale.ROOT);
        boolean anyMatch = false;
        for (int i = 0; i < sAudioTypes.size(); i++) {
            final boolean match = lowPath
                    .contains('/' + sAudioTypes.keyAt(i).toLowerCase(Locale.ROOT) + '/');
            op.withValue(sAudioTypes.valueAt(i), match ? 1 : 0);
            anyMatch |= match;
        }
        if (!anyMatch) {
            op.withValue(AudioColumns.IS_MUSIC, 1);
        }

        try (FileInputStream is = new FileInputStream(file)) {
            try (MediaMetadataRetriever mmr = new MediaMetadataRetriever()) {
                mmr.setDataSource(is.getFD());

                withOptionalValue(op, MediaColumns.TITLE,
                        parseOptional(mmr.extractMetadata(METADATA_KEY_TITLE)));
                withOptionalValue(op, MediaColumns.IS_DRM,
                        parseOptional(mmr.extractMetadata(METADATA_KEY_IS_DRM)));
                withOptionalValue(op, MediaColumns.DURATION,
                        parseOptional(mmr.extractMetadata(METADATA_KEY_DURATION)));

                withOptionalValue(op, AudioColumns.ARTIST,
                        parseOptional(mmr.extractMetadata(METADATA_KEY_ARTIST)));
                withOptionalValue(op, AudioColumns.ALBUM_ARTIST,
                        parseOptional(mmr.extractMetadata(METADATA_KEY_ALBUMARTIST)));
                withOptionalValue(op, AudioColumns.COMPILATION,
                        parseOptional(mmr.extractMetadata(METADATA_KEY_COMPILATION)));
                withOptionalValue(op, AudioColumns.COMPOSER,
                        parseOptional(mmr.extractMetadata(METADATA_KEY_COMPOSER)));
                withOptionalValue(op, AudioColumns.ALBUM,
                        parseOptional(mmr.extractMetadata(METADATA_KEY_ALBUM)));
                withOptionalValue(op, AudioColumns.TRACK,
                        parseOptional(mmr.extractMetadata(METADATA_KEY_CD_TRACK_NUMBER)));
                withOptionalValue(op, AudioColumns.YEAR,
                        parseOptionalOrZero(mmr.extractMetadata(METADATA_KEY_YEAR)));
                withOptionalValue(op, AudioColumns.GENRE,
                        parseOptional(mmr.extractMetadata(METADATA_KEY_GENRE)));
            }

            // Also hunt around for XMP metadata
            final IsoInterface iso = IsoInterface.fromFileDescriptor(is.getFD());
            final XmpInterface xmp = XmpInterface.fromContainer(iso);
            withXmpValues(op, xmp, mimeType);

        } catch (Exception e) {
            throw new IOException(e);
        }
        return op.build();
    }

    private static @NonNull ContentProviderOperation scanItemPlaylist(long existingId, File file,
            BasicFileAttributes attrs, String mimeType, String volumeName) throws IOException {
        final ContentProviderOperation.Builder op = newUpsert(
                MediaStore.Audio.Playlists.getContentUri(volumeName), existingId);
        try {
            withGenericValues(op, file, attrs, mimeType);
            op.withValue(PlaylistsColumns.NAME, extractName(file));
        } catch (Exception e) {
            throw new IOException(e);
        }
        return op.build();
    }

    private static @NonNull ContentProviderOperation scanItemVideo(long existingId, File file,
            BasicFileAttributes attrs, String mimeType, String volumeName) throws IOException {
        final ContentProviderOperation.Builder op = newUpsert(
                MediaStore.Video.Media.getContentUri(volumeName), existingId);

        withGenericValues(op, file, attrs, mimeType);
        op.withValue(VideoColumns.ARTIST, UNKNOWN_STRING);
        op.withValue(VideoColumns.ALBUM, file.getParentFile().getName());
        op.withValue(VideoColumns.RESOLUTION, null);
        op.withValue(VideoColumns.COLOR_STANDARD, null);
        op.withValue(VideoColumns.COLOR_TRANSFER, null);
        op.withValue(VideoColumns.COLOR_RANGE, null);

        try (FileInputStream is = new FileInputStream(file)) {
            try (MediaMetadataRetriever mmr = new MediaMetadataRetriever()) {
                mmr.setDataSource(is.getFD());

                withOptionalValue(op, MediaColumns.TITLE,
                        parseOptional(mmr.extractMetadata(METADATA_KEY_TITLE)));
                withOptionalValue(op, MediaColumns.IS_DRM,
                        parseOptional(mmr.extractMetadata(METADATA_KEY_IS_DRM)));
                withOptionalValue(op, MediaColumns.WIDTH,
                        parseOptional(mmr.extractMetadata(METADATA_KEY_VIDEO_WIDTH)));
                withOptionalValue(op, MediaColumns.HEIGHT,
                        parseOptional(mmr.extractMetadata(METADATA_KEY_VIDEO_HEIGHT)));
                withOptionalValue(op, MediaColumns.DURATION,
                        parseOptional(mmr.extractMetadata(METADATA_KEY_DURATION)));
                withOptionalValue(op, MediaColumns.DATE_TAKEN,
                        parseOptionalDate(mmr.extractMetadata(METADATA_KEY_DATE)));

                withOptionalValue(op, VideoColumns.ARTIST,
                        parseOptional(mmr.extractMetadata(METADATA_KEY_ARTIST)));
                withOptionalValue(op, VideoColumns.ALBUM,
                        parseOptional(mmr.extractMetadata(METADATA_KEY_ALBUM)));
                withOptionalValue(op, VideoColumns.RESOLUTION,
                        parseOptionalResolution(mmr));
                withOptionalValue(op, VideoColumns.COLOR_STANDARD,
                        parseOptional(mmr.extractMetadata(METADATA_KEY_COLOR_STANDARD)));
                withOptionalValue(op, VideoColumns.COLOR_TRANSFER,
                        parseOptional(mmr.extractMetadata(METADATA_KEY_COLOR_TRANSFER)));
                withOptionalValue(op, VideoColumns.COLOR_RANGE,
                        parseOptional(mmr.extractMetadata(METADATA_KEY_COLOR_RANGE)));
            }

            // Also hunt around for XMP metadata
            final IsoInterface iso = IsoInterface.fromFileDescriptor(is.getFD());
            final XmpInterface xmp = XmpInterface.fromContainer(iso);
            withXmpValues(op, xmp, mimeType);

        } catch (Exception e) {
            throw new IOException(e);
        }
        return op.build();
    }

    private static @NonNull ContentProviderOperation scanItemImage(long existingId, File file,
            BasicFileAttributes attrs, String mimeType, String volumeName) throws IOException {
        final ContentProviderOperation.Builder op = newUpsert(
                MediaStore.Images.Media.getContentUri(volumeName), existingId);

        withGenericValues(op, file, attrs, mimeType);
        op.withValue(ImageColumns.DESCRIPTION, null);

        try (FileInputStream is = new FileInputStream(file)) {
            final ExifInterface exif = new ExifInterface(is);

            withOptionalValue(op, MediaColumns.WIDTH,
                    parseOptionalOrZero(exif.getAttribute(ExifInterface.TAG_IMAGE_WIDTH)));
            withOptionalValue(op, MediaColumns.HEIGHT,
                    parseOptionalOrZero(exif.getAttribute(ExifInterface.TAG_IMAGE_LENGTH)));
            withOptionalValue(op, MediaColumns.DATE_TAKEN,
                    parseOptionalDateTaken(exif, lastModifiedTime(file, attrs) * 1000));
            withOptionalValue(op, MediaColumns.ORIENTATION,
                    parseOptionalOrientation(exif.getAttributeInt(ExifInterface.TAG_ORIENTATION,
                            ExifInterface.ORIENTATION_UNDEFINED)));

            withOptionalValue(op, ImageColumns.DESCRIPTION,
                    parseOptional(exif.getAttribute(ExifInterface.TAG_IMAGE_DESCRIPTION)));

            // Also hunt around for XMP metadata
            final XmpInterface xmp = XmpInterface.fromContainer(exif);
            withXmpValues(op, xmp, mimeType);

        } catch (Exception e) {
            throw new IOException(e);
        }
        return op.build();
    }

    private static @NonNull ContentProviderOperation scanItemFile(long existingId, File file,
            BasicFileAttributes attrs, String mimeType, String volumeName) throws IOException {
        final ContentProviderOperation.Builder op = newUpsert(
                MediaStore.Files.getContentUri(volumeName), existingId);
        try {
            withGenericValues(op, file, attrs, mimeType);
        } catch (Exception e) {
            throw new IOException(e);
        }
        return op.build();
    }

    private static @NonNull ContentProviderOperation.Builder newUpsert(Uri uri, long existingId) {
        if (existingId == -1) {
            return ContentProviderOperation.newInsert(uri)
                    .withFailureAllowed(true);
        } else {
            return ContentProviderOperation.newUpdate(ContentUris.withAppendedId(uri, existingId))
                    .withExpectedCount(1)
                    .withFailureAllowed(true);
        }
    }

    public static @Nullable String extractExtension(File file) {
        final String name = file.getName();
        final int lastDot = name.lastIndexOf('.');
        return (lastDot == -1) ? null : name.substring(lastDot + 1);
    }

    public static @NonNull String extractName(File file) {
        final String name = file.getName();
        final int lastDot = name.lastIndexOf('.');
        return (lastDot == -1) ? name : name.substring(0, lastDot);
    }

    private static @NonNull <T> Optional<T> parseOptional(@Nullable T value) {
        if (value == null) {
            return Optional.empty();
        } else if (value instanceof String && ((String) value).length() == 0) {
            return Optional.empty();
        } else if (value instanceof String && ((String) value).equals("-1")) {
            return Optional.empty();
        } else if (value instanceof Number && ((Number) value).intValue() == -1) {
            return Optional.empty();
        } else {
            return Optional.of(value);
        }
    }

    private static @NonNull <T> Optional<T> parseOptionalOrZero(@Nullable T value) {
        if (value instanceof String && ((String) value).equals("0")) {
            return Optional.empty();
        } else if (value instanceof Number && ((Number) value).intValue() == 0) {
            return Optional.empty();
        } else {
            return parseOptional(value);
        }
    }

    /**
     * Try our best to calculate {@link MediaColumns#DATE_TAKEN} in reference to
     * the epoch, making our best guess from unrelated fields when offset
     * information isn't directly available.
     */
    static @NonNull Optional<Long> parseOptionalDateTaken(@NonNull ExifInterface exif,
            @CurrentTimeMillisLong long lastModifiedTime) {
        final long originalTime = exif.getDateTimeOriginal();
        if (exif.hasAttribute(ExifInterface.TAG_OFFSET_TIME_ORIGINAL)) {
            // We have known offset information, return it directly!
            return Optional.of(originalTime);
        } else {
            // Otherwise we need to guess the offset from unrelated fields
            final long smallestZone = 15 * MINUTE_IN_MILLIS;
            final long gpsTime = exif.getGpsDateTime();
            if (gpsTime > 0) {
                final long offset = gpsTime - originalTime;
                if (Math.abs(offset) < 24 * HOUR_IN_MILLIS) {
                    final long rounded = Math.round((float) offset / smallestZone) * smallestZone;
                    return Optional.of(originalTime + rounded);
                }
            }
            if (lastModifiedTime > 0) {
                final long offset = lastModifiedTime - originalTime;
                if (Math.abs(offset) < 24 * HOUR_IN_MILLIS) {
                    final long rounded = Math.round((float) offset / smallestZone) * smallestZone;
                    return Optional.of(originalTime + rounded);
                }
            }
            return Optional.empty();
        }
    }

    private static @NonNull Optional<Integer> parseOptionalOrientation(int orientation) {
        switch (orientation) {
            case ExifInterface.ORIENTATION_NORMAL: return Optional.of(0);
            case ExifInterface.ORIENTATION_ROTATE_90: return Optional.of(90);
            case ExifInterface.ORIENTATION_ROTATE_180: return Optional.of(180);
            case ExifInterface.ORIENTATION_ROTATE_270: return Optional.of(270);
            default: return Optional.empty();
        }
    }

    private static @NonNull Optional<String> parseOptionalResolution(
            @NonNull MediaMetadataRetriever mmr) {
        final Optional<?> width = parseOptional(mmr.extractMetadata(METADATA_KEY_VIDEO_WIDTH));
        final Optional<?> height = parseOptional(mmr.extractMetadata(METADATA_KEY_VIDEO_HEIGHT));
        if (width.isPresent() && height.isPresent()) {
            return Optional.of(width.get() + "\u00d7" + height.get());
        } else {
            return Optional.empty();
        }
    }

    private static @NonNull Optional<Long> parseOptionalDate(@Nullable String date) {
        if (TextUtils.isEmpty(date)) return Optional.empty();
        try {
            final long value = sDateFormat.parse(date).getTime();
            return (value > 0) ? Optional.of(value) : Optional.empty();
        } catch (ParseException e) {
            return Optional.empty();
        }
    }

    /**
     * Maybe replace the MIME type from extension with the MIME type from the
     * XMP metadata, but only when the top-level MIME type agrees.
     */
    @VisibleForTesting
    public static @NonNull String maybeOverrideMimeType(@NonNull String extMimeType,
            @Nullable String xmpMimeType) {
        // Ignore XMP when missing
        if (TextUtils.isEmpty(xmpMimeType)) return extMimeType;

        // Ignore XMP when invalid
        final int xmpSplit = xmpMimeType.indexOf('/');
        if (xmpSplit == -1) return extMimeType;

        if (extMimeType.regionMatches(0, xmpMimeType, 0, xmpSplit + 1)) {
            return xmpMimeType;
        } else {
            return extMimeType;
        }
    }

    /**
     * Return last modified time of given file. This value is typically read
     * from the given {@link BasicFileAttributes}, except in the case of
     * read-only partitions, where {@link Build#TIME} is used instead.
     */
    public static @CurrentTimeSecondsLong long lastModifiedTime(@NonNull File file,
            @NonNull BasicFileAttributes attrs) {
        if (FileUtils.contains(Environment.getStorageDirectory(), file)) {
            return attrs.lastModifiedTime().toMillis() / 1000;
        } else {
            return Build.TIME / 1000;
        }
    }

    /**
     * Test if any parents of given directory should be considered hidden.
     */
    static boolean isDirectoryHiddenRecursive(File dir) {
        Trace.traceBegin(TRACE_TAG_DATABASE, "isDirectoryHiddenRecursive");
        try {
            while (dir != null) {
                if (isDirectoryHidden(dir)) {
                    return true;
                }
                dir = dir.getParentFile();
            }
            return false;
        } finally {
            Trace.traceEnd(TRACE_TAG_DATABASE);
        }
    }

    /**
     * Test if this given directory should be considered hidden.
     */
    static boolean isDirectoryHidden(File dir) {
        final File nomedia = new File(dir, ".nomedia");

        // Handle well-known paths that should always be visible or invisible,
        // regardless of .nomedia presence
        if (PATTERN_VISIBLE.matcher(dir.getAbsolutePath()).matches()) {
            nomedia.delete();
            return false;
        }
        if (PATTERN_INVISIBLE.matcher(dir.getAbsolutePath()).matches()) {
            try {
                nomedia.createNewFile();
            } catch (IOException ignored) {
            }
            return true;
        }

        // Otherwise fall back to directory name or .nomedia presence
        final String name = dir.getName();
        if (name.startsWith(".")) {
            return true;
        }
        if (nomedia.exists()) {
            return true;
        }
        return false;
    }

    /**
     * Test if this given {@link Uri} is a
     * {@link android.provider.MediaStore.Audio.Playlists} item.
     */
    static boolean isPlaylist(Uri uri) {
        final List<String> path = uri.getPathSegments();
        return (path.size() == 4) && path.get(1).equals("audio") && path.get(2).equals("playlists");
    }

    /**
     * Escape the given argument for use in a {@code LIKE} statement.
     */
    static String escapeForLike(String arg) {
        final StringBuilder sb = new StringBuilder();
        for (int i = 0; i < arg.length(); i++) {
            final char c = arg.charAt(i);
            switch (c) {
                case '%': sb.append('\\');
                case '_': sb.append('\\');
            }
            sb.append(c);
        }
        return sb.toString();
    }
}
