// Copyright (C) 2020 Intel Corporation
//
// SPDX-License-Identifier: MIT

import { AnyAction, Dispatch, ActionCreator } from 'redux';
import { ThunkAction } from 'redux-thunk';
import {
    TasksQuery,
    CombinedState,
} from 'reducers/interfaces';
import { getCVATStore } from 'cvat-store';
import getCore from 'cvat-core-wrapper';
import { getInferenceStatusAsync } from './models-actions';

const cvat = getCore();

export enum TasksActionTypes {
    GET_TASKS = 'GET_TASKS',
    GET_TASKS_SUCCESS = 'GET_TASKS_SUCCESS',
    GET_TASKS_FAILED = 'GET_TASKS_FAILED',
    LOAD_ANNOTATIONS = 'LOAD_ANNOTATIONS',
    LOAD_ANNOTATIONS_SUCCESS = 'LOAD_ANNOTATIONS_SUCCESS',
    LOAD_ANNOTATIONS_FAILED = 'LOAD_ANNOTATIONS_FAILED',
    DUMP_ANNOTATIONS = 'DUMP_ANNOTATIONS',
    DUMP_ANNOTATIONS_SUCCESS = 'DUMP_ANNOTATIONS_SUCCESS',
    DUMP_ANNOTATIONS_FAILED = 'DUMP_ANNOTATIONS_FAILED',
    EXPORT_DATASET = 'EXPORT_DATASET',
    EXPORT_DATASET_SUCCESS = 'EXPORT_DATASET_SUCCESS',
    EXPORT_DATASET_FAILED = 'EXPORT_DATASET_FAILED',
    DELETE_TASK = 'DELETE_TASK',
    DELETE_TASK_SUCCESS = 'DELETE_TASK_SUCCESS',
    DELETE_TASK_FAILED = 'DELETE_TASK_FAILED',
    CREATE_TASK = 'CREATE_TASK',
    CREATE_TASK_STATUS_UPDATED = 'CREATE_TASK_STATUS_UPDATED',
    CREATE_TASK_SUCCESS = 'CREATE_TASK_SUCCESS',
    CREATE_TASK_FAILED = 'CREATE_TASK_FAILED',
    UPDATE_TASK = 'UPDATE_TASK',
    UPDATE_TASK_SUCCESS = 'UPDATE_TASK_SUCCESS',
    UPDATE_TASK_FAILED = 'UPDATE_TASK_FAILED',
    HIDE_EMPTY_TASKS = 'HIDE_EMPTY_TASKS',
}

function getTasks(): AnyAction {
    const action = {
        type: TasksActionTypes.GET_TASKS,
        payload: {},
    };

    return action;
}

function getTasksSuccess(array: any[], previews: string[],
    count: number, query: TasksQuery): AnyAction {
    const action = {
        type: TasksActionTypes.GET_TASKS_SUCCESS,
        payload: {
            previews,
            array,
            count,
            query,
        },
    };

    return action;
}

function getTasksFailed(error: any, query: TasksQuery): AnyAction {
    const action = {
        type: TasksActionTypes.GET_TASKS_FAILED,
        payload: {
            error,
            query,
        },
    };

    return action;
}

export function getTasksAsync(query: TasksQuery):
ThunkAction<Promise<void>, {}, {}, AnyAction> {
    return async (dispatch: ActionCreator<Dispatch>): Promise<void> => {
        dispatch(getTasks());

        // We need remove all keys with null values from query
        const filteredQuery = { ...query };
        for (const key in filteredQuery) {
            if (filteredQuery[key] === null) {
                delete filteredQuery[key];
            }
        }

        let result = null;
        try {
            result = await cvat.tasks.get(filteredQuery);
        } catch (error) {
            dispatch(getTasksFailed(error, query));
            return;
        }

        const array = Array.from(result);
        const previews = [];
        const promises = array
            .map((task): string => (task as any).frames.preview());

        dispatch(
            getInferenceStatusAsync(
                array.map(
                    (task: any): number => task.id,
                ),
            ),
        );

        for (const promise of promises) {
            try {
                // a tricky moment
                // await is okay in loop in this case, there aren't any performance bottleneck
                // because all server requests have been already sent in parallel

                // eslint-disable-next-line no-await-in-loop
                previews.push(await promise);
            } catch (error) {
                previews.push('');
            }
        }

        dispatch(getTasksSuccess(array, previews, result.count, query));
    };
}

function dumpAnnotation(task: any, dumper: any): AnyAction {
    const action = {
        type: TasksActionTypes.DUMP_ANNOTATIONS,
        payload: {
            task,
            dumper,
        },
    };

    return action;
}

function dumpAnnotationSuccess(task: any, dumper: any): AnyAction {
    const action = {
        type: TasksActionTypes.DUMP_ANNOTATIONS_SUCCESS,
        payload: {
            task,
            dumper,
        },
    };

    return action;
}

function dumpAnnotationFailed(task: any, dumper: any, error: any): AnyAction {
    const action = {
        type: TasksActionTypes.DUMP_ANNOTATIONS_FAILED,
        payload: {
            task,
            dumper,
            error,
        },
    };

    return action;
}

export function dumpAnnotationsAsync(task: any, dumper: any):
ThunkAction<Promise<void>, {}, {}, AnyAction> {
    return async (dispatch: ActionCreator<Dispatch>): Promise<void> => {
        try {
            dispatch(dumpAnnotation(task, dumper));
            const url = await task.annotations.dump(dumper);
            const downloadAnchor = (window.document.getElementById('downloadAnchor') as HTMLAnchorElement);
            downloadAnchor.href = url;
            downloadAnchor.click();
        } catch (error) {
            dispatch(dumpAnnotationFailed(task, dumper, error));
            return;
        }

        dispatch(dumpAnnotationSuccess(task, dumper));
    };
}

function loadAnnotations(task: any, loader: any): AnyAction {
    const action = {
        type: TasksActionTypes.LOAD_ANNOTATIONS,
        payload: {
            task,
            loader,
        },
    };

    return action;
}

function loadAnnotationsSuccess(task: any): AnyAction {
    const action = {
        type: TasksActionTypes.LOAD_ANNOTATIONS_SUCCESS,
        payload: {
            task,
        },
    };

    return action;
}

function loadAnnotationsFailed(task: any, error: any): AnyAction {
    const action = {
        type: TasksActionTypes.LOAD_ANNOTATIONS_FAILED,
        payload: {
            task,
            error,
        },
    };

    return action;
}

export function loadAnnotationsAsync(task: any, loader: any, file: File):
ThunkAction<Promise<void>, {}, {}, AnyAction> {
    return async (dispatch: ActionCreator<Dispatch>): Promise<void> => {
        try {
            const store = getCVATStore();
            const state: CombinedState = store.getState();
            if (state.tasks.activities.loads[task.id]) {
                throw Error('Only one loading of annotations for a task allowed at the same time');
            }
            dispatch(loadAnnotations(task, loader));
            await task.annotations.upload(file, loader);
        } catch (error) {
            dispatch(loadAnnotationsFailed(task, error));
            return;
        }

        dispatch(loadAnnotationsSuccess(task));
    };
}

function exportDataset(task: any, exporter: any): AnyAction {
    const action = {
        type: TasksActionTypes.EXPORT_DATASET,
        payload: {
            task,
            exporter,
        },
    };

    return action;
}

function exportDatasetSuccess(task: any, exporter: any): AnyAction {
    const action = {
        type: TasksActionTypes.EXPORT_DATASET_SUCCESS,
        payload: {
            task,
            exporter,
        },
    };

    return action;
}

function exportDatasetFailed(task: any, exporter: any, error: any): AnyAction {
    const action = {
        type: TasksActionTypes.EXPORT_DATASET_FAILED,
        payload: {
            task,
            exporter,
            error,
        },
    };

    return action;
}

export function exportDatasetAsync(task: any, exporter: any):
ThunkAction<Promise<void>, {}, {}, AnyAction> {
    return async (dispatch: ActionCreator<Dispatch>): Promise<void> => {
        dispatch(exportDataset(task, exporter));

        try {
            const url = await task.annotations.exportDataset(exporter.name);
            const downloadAnchor = (window.document.getElementById('downloadAnchor') as HTMLAnchorElement);
            downloadAnchor.href = url;
            downloadAnchor.click();
        } catch (error) {
            dispatch(exportDatasetFailed(task, exporter, error));
        }

        dispatch(exportDatasetSuccess(task, exporter));
    };
}

function deleteTask(taskID: number): AnyAction {
    const action = {
        type: TasksActionTypes.DELETE_TASK,
        payload: {
            taskID,
        },
    };

    return action;
}

function deleteTaskSuccess(taskID: number): AnyAction {
    const action = {
        type: TasksActionTypes.DELETE_TASK_SUCCESS,
        payload: {
            taskID,
        },
    };

    return action;
}

function deleteTaskFailed(taskID: number, error: any): AnyAction {
    const action = {
        type: TasksActionTypes.DELETE_TASK_FAILED,
        payload: {
            taskID,
            error,
        },
    };

    return action;
}

export function deleteTaskAsync(taskInstance: any):
ThunkAction<Promise<void>, {}, {}, AnyAction> {
    return async (dispatch: ActionCreator<Dispatch>): Promise<void> => {
        try {
            dispatch(deleteTask(taskInstance.id));
            await taskInstance.delete();
        } catch (error) {
            dispatch(deleteTaskFailed(taskInstance.id, error));
            return;
        }

        dispatch(deleteTaskSuccess(taskInstance.id));
    };
}

function createTask(): AnyAction {
    const action = {
        type: TasksActionTypes.CREATE_TASK,
        payload: {},
    };

    return action;
}

function createTaskSuccess(): AnyAction {
    const action = {
        type: TasksActionTypes.CREATE_TASK_SUCCESS,
        payload: {},
    };

    return action;
}

function createTaskFailed(error: any): AnyAction {
    const action = {
        type: TasksActionTypes.CREATE_TASK_FAILED,
        payload: {
            error,
        },
    };

    return action;
}

function createTaskUpdateStatus(status: string): AnyAction {
    const action = {
        type: TasksActionTypes.CREATE_TASK_STATUS_UPDATED,
        payload: {
            status,
        },
    };

    return action;
}

export function createTaskAsync(data: any):
ThunkAction<Promise<void>, {}, {}, AnyAction> {
    return async (dispatch: ActionCreator<Dispatch>): Promise<void> => {
        const description: any = {
            name: data.basic.name,
            labels: data.labels,
            z_order: data.advanced.zOrder,
            image_quality: 70,
            use_zip_chunks: data.advanced.useZipChunks,
        };

        if (data.advanced.bugTracker) {
            description.bug_tracker = data.advanced.bugTracker;
        }
        if (data.advanced.segmentSize) {
            description.segment_size = data.advanced.segmentSize;
        }
        if (data.advanced.overlapSize) {
            description.overlap = data.advanced.overlapSize;
        }
        if (data.advanced.startFrame) {
            description.start_frame = data.advanced.startFrame;
        }
        if (data.advanced.stopFrame) {
            description.stop_frame = data.advanced.stopFrame;
        }
        if (data.advanced.frameFilter) {
            description.frame_filter = data.advanced.frameFilter;
        }
        if (data.advanced.imageQuality) {
            description.image_quality = data.advanced.imageQuality;
        }
        if (data.advanced.dataChunkSize) {
            description.data_chunk_size = data.advanced.dataChunkSize;
        }

        const taskInstance = new cvat.classes.Task(description);
        taskInstance.clientFiles = data.files.local;
        taskInstance.serverFiles = data.files.share;
        taskInstance.remoteFiles = data.files.remote;

        if (data.advanced.repository) {
            const [gitPlugin] = (await cvat.plugins.list()).filter(
                (plugin: any): boolean => plugin.name === 'Git',
            );

            if (gitPlugin) {
                gitPlugin.callbacks.onStatusChange = (status: string): void => {
                    dispatch(createTaskUpdateStatus(status));
                };
                gitPlugin.data.task = taskInstance;
                gitPlugin.data.repos = data.advanced.repository;
                gitPlugin.data.lfs = data.advanced.lfs;
            }
        }

        dispatch(createTask());
        try {
            await taskInstance.save((status: string): void => {
                dispatch(createTaskUpdateStatus(status));
            });
            dispatch(createTaskSuccess());
        } catch (error) {
            dispatch(createTaskFailed(error));
        }
    };
}

function updateTask(): AnyAction {
    const action = {
        type: TasksActionTypes.UPDATE_TASK,
        payload: {},
    };

    return action;
}

function updateTaskSuccess(task: any): AnyAction {
    const action = {
        type: TasksActionTypes.UPDATE_TASK_SUCCESS,
        payload: {
            task,
        },
    };

    return action;
}

function updateTaskFailed(error: any, task: any): AnyAction {
    const action = {
        type: TasksActionTypes.UPDATE_TASK_FAILED,
        payload: {
            error,
            task,
        },
    };

    return action;
}

export function updateTaskAsync(taskInstance: any):
ThunkAction<Promise<void>, {}, {}, AnyAction> {
    return async (dispatch: ActionCreator<Dispatch>): Promise<void> => {
        try {
            dispatch(updateTask());
            await taskInstance.save();
            const [task] = await cvat.tasks.get({ id: taskInstance.id });
            dispatch(updateTaskSuccess(task));
        } catch (error) {
            // try abort all changes
            let task = null;
            try {
                [task] = await cvat.tasks.get({ id: taskInstance.id });
            } catch (fetchError) {
                dispatch(updateTaskFailed(error, taskInstance));
                return;
            }

            dispatch(updateTaskFailed(error, task));
        }
    };
}

// a job is a part of a task, so for simplify we consider
// updating the job as updating a task
export function updateJobAsync(jobInstance: any):
ThunkAction<Promise<void>, {}, {}, AnyAction> {
    return async (dispatch: ActionCreator<Dispatch>): Promise<void> => {
        try {
            dispatch(updateTask());
            await jobInstance.save();
            const [task] = await cvat.tasks.get({ id: jobInstance.task.id });
            dispatch(updateTaskSuccess(task));
        } catch (error) {
            // try abort all changes
            let task = null;
            try {
                [task] = await cvat.tasks.get({ id: jobInstance.task.id });
            } catch (fetchError) {
                dispatch(updateTaskFailed(error, jobInstance.task));
                return;
            }

            dispatch(updateTaskFailed(error, task));
        }
    };
}

export function hideEmptyTasks(hideEmpty: boolean): AnyAction {
    const action = {
        type: TasksActionTypes.HIDE_EMPTY_TASKS,
        payload: {
            hideEmpty,
        },
    };

    return action;
}
